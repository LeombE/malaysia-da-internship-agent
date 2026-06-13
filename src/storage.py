from __future__ import annotations

import csv
import json
import re
import sqlite3
from pathlib import Path
from typing import Iterable

from .models import JobPosting, utc_now_iso


SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    job_id TEXT PRIMARY KEY,
    source TEXT,
    title TEXT,
    company TEXT,
    location TEXT,
    state TEXT,
    description TEXT,
    apply_url TEXT,
    source_url TEXT,
    posted_at TEXT,
    salary TEXT,
    score INTEGER,
    reasons TEXT,
    raw_json TEXT,
    first_seen_at TEXT,
    last_seen_at TEXT,
    notify_count INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS run_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ran_at TEXT,
    source TEXT,
    status TEXT,
    message TEXT,
    item_count INTEGER DEFAULT 0
);
"""


def _norm(value: str | None) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def _bucket(score: int) -> str:
    if score >= 70:
        return "A_APPLY_NOW"
    if score >= 55:
        return "B_APPLY_SOON"
    if score >= 42:
        return "C_MASS_APPLY"
    return "D_LOW_PRIORITY"


def _action(bucket: str) -> str:
    return {
        "A_APPLY_NOW": "Apply today; verify date/duration first.",
        "B_APPLY_SOON": "Apply within 48 hours after quick verification.",
        "C_MASS_APPLY": "Mass-apply if role/location is acceptable.",
        "D_LOW_PRIORITY": "Ignore unless manually relevant.",
    }.get(bucket, "Review manually.")


def _canonical_key(row: dict) -> str:
    title = _norm(row.get("title"))
    company = _norm(row.get("company"))
    state = _norm(row.get("state") or row.get("location"))
    title = re.sub(r"\b(internship|intern|trainee|practical training|industrial training)\b", "intern", title)
    return f"{title}|{company}|{state}"


def _source_rank(row: dict) -> int:
    url = _norm((row.get("apply_url") or "") + " " + (row.get("source_url") or ""))
    if any(x in url for x in ["careers", "workdayjobs", "myworkdayjobs", "successfactors", "greenhouse", "lever", "smartrecruiters"]):
        return 3
    if any(x in url for x in ["jobstreet", "linkedin", "hiredly", "indeed", "foundit"]):
        return 2
    if any(x in url for x in [
        "trabajo", "jobleads", "jooble", "expertini", "bebee", "grabjobs", "prosple",
        "whatjobs", "talent", "jora", "maukerja", "builtin", "adzuna", "freelancing",
    ]):
        return 0
    return 1


def _enrich(row: dict) -> dict:
    row = dict(row)
    score = int(row.get("score") or 0)
    bucket = _bucket(score)
    row["bucket"] = bucket
    row["recommended_action"] = _action(bucket)
    row["source_rank"] = _source_rank(row)
    return row


class JobStore:
    def __init__(self, db_path: str) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def close(self) -> None:
        try:
            self.conn.execute("PRAGMA wal_checkpoint(FULL)")
            self.conn.commit()
        finally:
            self.conn.close()

    def upsert_jobs(self, jobs: Iterable[JobPosting]) -> tuple[int, int]:
        new_count = 0
        update_count = 0
        now = utc_now_iso()
        for job in jobs:
            existing = self.conn.execute("SELECT job_id FROM jobs WHERE job_id = ?", (job.job_id,)).fetchone()
            if existing:
                update_count += 1
                self.conn.execute(
                    """
                    UPDATE jobs SET
                        source=?, title=?, company=?, location=?, state=?, description=?, apply_url=?, source_url=?,
                        posted_at=?, salary=?, score=?, reasons=?, raw_json=?, last_seen_at=?
                    WHERE job_id=?
                    """,
                    (
                        job.source, job.title, job.company, job.location, job.state, job.description, job.apply_url,
                        job.source_url, job.posted_at, job.salary, job.score, "; ".join(job.reasons),
                        json.dumps(job.raw, ensure_ascii=False), now, job.job_id,
                    ),
                )
            else:
                new_count += 1
                self.conn.execute(
                    """
                    INSERT INTO jobs (
                        job_id, source, title, company, location, state, description, apply_url, source_url,
                        posted_at, salary, score, reasons, raw_json, first_seen_at, last_seen_at, notify_count
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
                    """,
                    (
                        job.job_id, job.source, job.title, job.company, job.location, job.state, job.description,
                        job.apply_url, job.source_url, job.posted_at, job.salary, job.score, "; ".join(job.reasons),
                        json.dumps(job.raw, ensure_ascii=False), now, now,
                    ),
                )
        self.conn.commit()
        return new_count, update_count

    def top_jobs(self, limit: int = 40, min_score: int = 0, only_unnotified: bool = False, dedupe: bool = True) -> list[dict]:
        where = ["score >= ?"]
        params: list = [min_score]
        if only_unnotified:
            where.append("notify_count = 0")
        query = f"""
            SELECT job_id, source, title, company, location, state, description, apply_url, source_url,
                   posted_at, salary, score, reasons, first_seen_at, last_seen_at, notify_count
            FROM jobs
            WHERE {' AND '.join(where)}
            ORDER BY score DESC, last_seen_at DESC, first_seen_at DESC
            LIMIT 2000
        """
        cur = self.conn.execute(query, params)
        cols = [d[0] for d in cur.description]
        rows = [_enrich(dict(zip(cols, row))) for row in cur.fetchall()]

        if dedupe:
            best: dict[str, dict] = {}
            for row in rows:
                key = _canonical_key(row)
                if not key.strip("|"):
                    key = str(row.get("job_id"))
                current = best.get(key)
                if current is None:
                    best[key] = row
                    continue
                candidate_tuple = (int(row.get("source_rank") or 0), int(row.get("score") or 0), str(row.get("last_seen_at") or ""))
                current_tuple = (int(current.get("source_rank") or 0), int(current.get("score") or 0), str(current.get("last_seen_at") or ""))
                if candidate_tuple > current_tuple:
                    best[key] = row
            rows = list(best.values())

        rows.sort(key=lambda r: (int(r.get("score") or 0), int(r.get("source_rank") or 0), str(r.get("last_seen_at") or "")), reverse=True)
        return rows[:limit]

    def existing_jobs(self, limit: int = 5000) -> list[JobPosting]:
        query = """
            SELECT job_id, source, title, company, location, state, description, apply_url, source_url,
                   posted_at, salary, raw_json
            FROM jobs
            ORDER BY last_seen_at DESC
            LIMIT ?
        """
        rows = self.conn.execute(query, (limit,)).fetchall()
        jobs: list[JobPosting] = []
        for row in rows:
            raw = {}
            try:
                raw = json.loads(row[11] or "{}")
            except Exception:
                raw = {}
            jobs.append(JobPosting(
                job_id=row[0] or "",
                source=row[1] or "",
                title=row[2] or "",
                company=row[3] or "",
                location=row[4] or "",
                state=row[5] or "",
                description=row[6] or "",
                apply_url=row[7] or "",
                source_url=row[8] or "",
                posted_at=row[9] or "",
                salary=row[10] or "",
                raw=raw,
            ))
        return jobs

    def mark_notified(self, job_ids: list[str]) -> None:
        if not job_ids:
            return
        self.conn.executemany(
            "UPDATE jobs SET notify_count = notify_count + 1 WHERE job_id = ?",
            [(jid,) for jid in job_ids],
        )
        self.conn.commit()

    def log_run(self, source: str, status: str, message: str, item_count: int = 0) -> None:
        self.conn.execute(
            "INSERT INTO run_logs (ran_at, source, status, message, item_count) VALUES (?, ?, ?, ?, ?)",
            (utc_now_iso(), source, status, message, item_count),
        )
        self.conn.commit()

    def _write_rows(self, path: str, rows: list[dict], fieldnames: list[str] | None = None) -> None:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        if not rows:
            out.write_text("", encoding="utf-8")
            return
        if fieldnames is None:
            fieldnames = list(rows[0].keys())
        with out.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)

    def export_csv(self, path: str, limit: int = 500) -> None:
        rows = self.top_jobs(limit=limit, min_score=0, only_unnotified=False, dedupe=True)
        self._write_rows(path, rows)

    def export_shortlist_csv(self, path: str, limit: int = 80, min_score: int = 42) -> None:
        rows = self.top_jobs(limit=limit, min_score=min_score, only_unnotified=False, dedupe=True)
        fieldnames = [
            "bucket", "recommended_action", "score", "company", "title", "location", "state",
            "source", "apply_url", "source_url", "posted_at", "first_seen_at", "last_seen_at", "reasons",
            "job_id",
        ]
        self._write_rows(path, rows, fieldnames)

    def export_tracker_csv(self, path: str, min_score: int = 38) -> None:
        out = Path(path)
        existing: dict[str, dict] = {}
        if out.exists() and out.read_text(encoding="utf-8", errors="ignore").strip():
            with out.open("r", newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    if row.get("job_id"):
                        existing[row["job_id"]] = row

        rows = self.top_jobs(limit=500, min_score=min_score, only_unnotified=False, dedupe=True)
        tracker_rows: list[dict] = []
        for row in rows:
            old = existing.get(str(row.get("job_id")), {})
            tracker_rows.append({
                "job_id": row.get("job_id", ""),
                "bucket": row.get("bucket", ""),
                "recommended_action": row.get("recommended_action", ""),
                "applied": old.get("applied", ""),
                "application_date": old.get("application_date", ""),
                "status": old.get("status", ""),
                "follow_up_date": old.get("follow_up_date", ""),
                "interview_date": old.get("interview_date", ""),
                "offer_status": old.get("offer_status", ""),
                "notes": old.get("notes", ""),
                "score": row.get("score", ""),
                "company": row.get("company", ""),
                "title": row.get("title", ""),
                "location": row.get("location", ""),
                "state": row.get("state", ""),
                "source": row.get("source", ""),
                "apply_url": row.get("apply_url", ""),
                "source_url": row.get("source_url", ""),
                "first_seen_at": row.get("first_seen_at", ""),
                "last_seen_at": row.get("last_seen_at", ""),
                "reasons": row.get("reasons", ""),
            })

        fieldnames = [
            "job_id", "bucket", "recommended_action", "applied", "application_date", "status",
            "follow_up_date", "interview_date", "offer_status", "notes", "score", "company", "title",
            "location", "state", "source", "apply_url", "source_url", "first_seen_at", "last_seen_at", "reasons",
        ]
        self._write_rows(path, tracker_rows, fieldnames)
