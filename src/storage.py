from __future__ import annotations

import csv
import json
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


class JobStore:
    def __init__(self, db_path: str) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def close(self) -> None:
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

    def top_jobs(self, limit: int = 40, min_score: int = 0, only_unnotified: bool = False) -> list[dict]:
        where = ["score >= ?"]
        params: list = [min_score]
        if only_unnotified:
            where.append("notify_count = 0")
        query = f"""
            SELECT job_id, source, title, company, location, state, description, apply_url, source_url,
                   posted_at, salary, score, reasons, first_seen_at, last_seen_at, notify_count
            FROM jobs
            WHERE {' AND '.join(where)}
            ORDER BY score DESC, first_seen_at DESC
            LIMIT ?
        """
        params.append(limit)
        rows = self.conn.execute(query, params).fetchall()
        cols = [d[0] for d in self.conn.execute(query, params).description]
        return [dict(zip(cols, row)) for row in rows]

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

    def export_csv(self, path: str, limit: int = 200) -> None:
        rows = self.top_jobs(limit=limit, min_score=0, only_unnotified=False)
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        if not rows:
            out.write_text("", encoding="utf-8")
            return
        with out.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
