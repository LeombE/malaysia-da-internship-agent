from __future__ import annotations

import os
from typing import Any

import feedparser

from ..models import JobPosting


def enabled() -> bool:
    return bool(os.getenv("GOOGLE_ALERT_FEEDS", "").strip())


def fetch(config: dict[str, Any], per_feed: int = 20) -> list[JobPosting]:
    feeds = [x.strip() for x in os.getenv("GOOGLE_ALERT_FEEDS", "").split(",") if x.strip()]
    jobs: list[JobPosting] = []
    for feed_url in feeds:
        parsed = feedparser.parse(feed_url)
        for entry in parsed.entries[:per_feed]:
            title = getattr(entry, "title", "") or ""
            summary = getattr(entry, "summary", "") or ""
            link = getattr(entry, "link", "") or ""
            published = getattr(entry, "published", "") or getattr(entry, "updated", "") or ""
            # Google Alerts titles often look like: Job title - Company
            if " - " in title:
                t, c = title.split(" - ", 1)
            else:
                t, c = title, ""
            jobs.append(JobPosting(
                source="google_alerts",
                title=t,
                company=c,
                location="Malaysia",
                description=summary,
                apply_url=link,
                source_url=link,
                posted_at=published,
                raw=dict(entry),
            ))
    return jobs
