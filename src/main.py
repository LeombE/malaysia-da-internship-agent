from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Callable

import yaml
from dotenv import load_dotenv

from .models import JobPosting
from .scoring import score_job
from .storage import JobStore
from .notifications import format_jobs_message, send_telegram, send_email
from .sources import jsearch, adzuna, google_alerts, company_pages


SourceFetcher = Callable[[dict], list[JobPosting]]


def load_config(path: str = "config.yml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def collect_jobs(config: dict, store: JobStore) -> list[JobPosting]:
    sources: list[tuple[str, Callable[[], bool], SourceFetcher]] = [
        ("jsearch", jsearch.enabled, lambda cfg: jsearch.fetch(cfg)),
        ("adzuna", adzuna.enabled, lambda cfg: adzuna.fetch(cfg)),
        ("google_alerts", google_alerts.enabled, lambda cfg: google_alerts.fetch(cfg)),
        ("company_pages", company_pages.enabled, lambda cfg: company_pages.fetch(cfg)),
    ]

    all_jobs: list[JobPosting] = []
    for name, is_enabled, fetcher in sources:
        if not is_enabled():
            store.log_run(name, "skipped", "source not configured", 0)
            continue
        try:
            jobs = fetcher(config)
            store.log_run(name, "ok", "fetched successfully", len(jobs))
            all_jobs.extend(jobs)
        except Exception as exc:
            store.log_run(name, "error", str(exc), 0)
            print(f"[{name}] ERROR: {exc}")
    return all_jobs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Collect and score, but do not send notifications or mark notified.")
    parser.add_argument("--config", default="config.yml")
    args = parser.parse_args()

    load_dotenv()
    config = load_config(args.config)

    db_path = os.getenv("DB_PATH", "data/jobs.db")
    csv_path = os.getenv("CSV_EXPORT_PATH", "data/latest_ranked_jobs.csv")
    shortlist_path = os.getenv("SHORTLIST_EXPORT_PATH", "data/today_shortlist.csv")
    tracker_path = os.getenv("TRACKER_EXPORT_PATH", "data/internship_tracker.csv")
    max_results = int(os.getenv("MAX_RESULTS_PER_RUN", "120") or 120)
    min_score = int(os.getenv("MIN_SCORE_TO_NOTIFY", "42") or 42)
    shortlist_min_score = int(os.getenv("SHORTLIST_MIN_SCORE", "42") or 42)
    tracker_min_score = int(os.getenv("TRACKER_MIN_SCORE", "38") or 38)

    Path("data").mkdir(exist_ok=True)
    store = JobStore(db_path)
    try:
        jobs = collect_jobs(config, store)
        if os.getenv("RESCORE_EXISTING_DB", "1").strip().lower() not in {"0", "false", "no", "off"}:
            existing_jobs = store.existing_jobs()
            if existing_jobs:
                print(f"Rescoring existing DB jobs: {len(existing_jobs)}")
                jobs = existing_jobs + jobs

        scored = [score_job(job, config) for job in jobs]
        scored.sort(key=lambda j: j.score, reverse=True)
        if max_results:
            scored = scored[:max_results]

        new_count, updated_count = store.upsert_jobs(scored)
        store.export_csv(csv_path, limit=500)
        store.export_shortlist_csv(shortlist_path, limit=80, min_score=shortlist_min_score)
        store.export_tracker_csv(tracker_path, min_score=tracker_min_score)

        notify_jobs = store.top_jobs(limit=25, min_score=min_score, only_unnotified=True, dedupe=True)
        message = format_jobs_message(
            notify_jobs,
            title=f"Malaysia Data Analyst Internship Digest — new:{new_count} updated:{updated_count}",
        )

        print(message)
        print(f"\nCSV exported: {csv_path}")
        print(f"Shortlist exported: {shortlist_path}")
        print(f"Tracker exported: {tracker_path}")

        if not args.dry_run and notify_jobs:
            sent_any = False
            try:
                sent_any = send_telegram(message) or sent_any
            except Exception as exc:
                store.log_run("telegram", "error", str(exc), 0)
                print(f"[telegram] ERROR: {exc}")
            try:
                sent_any = send_email("Malaysia Data Analyst Internship Digest", message) or sent_any
            except Exception as exc:
                store.log_run("email", "error", str(exc), 0)
                print(f"[email] ERROR: {exc}")
            if sent_any:
                store.mark_notified([j["job_id"] for j in notify_jobs])
        return 0
    finally:
        store.close()


if __name__ == "__main__":
    raise SystemExit(main())
