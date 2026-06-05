from __future__ import annotations

import os
from typing import Any

import requests

from ..models import JobPosting


API_TEMPLATE = "https://api.adzuna.com/v1/api/jobs/my/search/{page}"


def enabled() -> bool:
    return bool(os.getenv("ADZUNA_APP_ID", "").strip() and os.getenv("ADZUNA_APP_KEY", "").strip())


def fetch(config: dict[str, Any], per_query: int = 10) -> list[JobPosting]:
    app_id = os.getenv("ADZUNA_APP_ID", "").strip()
    app_key = os.getenv("ADZUNA_APP_KEY", "").strip()
    if not app_id or not app_key:
        return []

    jobs: list[JobPosting] = []
    queries = config.get("queries", [])

    for item in queries:
        what = item.get("query", "")
        for loc in item.get("locations", ["Malaysia"]):
            params = {
                "app_id": app_id,
                "app_key": app_key,
                "results_per_page": per_query,
                "what": what,
                "where": loc,
                "content-type": "application/json",
            }
            try:
                response = requests.get(API_TEMPLATE.format(page=1), params=params, timeout=30)
                response.raise_for_status()
                payload = response.json()
            except Exception as exc:
                print(f"[adzuna] query failed: {what} / {loc}: {exc}")
                continue

            for row in payload.get("results", [])[:per_query]:
                company = (row.get("company") or {}).get("display_name") or ""
                location = (row.get("location") or {}).get("display_name") or loc
                jobs.append(JobPosting(
                    source="adzuna",
                    title=row.get("title") or "",
                    company=company,
                    location=location,
                    description=row.get("description") or "",
                    apply_url=row.get("redirect_url") or "",
                    source_url=row.get("redirect_url") or "",
                    posted_at=row.get("created") or "",
                    salary=f"{row.get('salary_min') or ''}-{row.get('salary_max') or ''}".strip("-"),
                    raw=row,
                ))
    return jobs
