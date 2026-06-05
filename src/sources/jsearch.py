from __future__ import annotations

from datetime import datetime, timezone
import os
from typing import Any

import requests

from ..models import JobPosting


API_URL = "https://api.openwebninja.com/jsearch/search-v2"


def enabled() -> bool:
    return bool(os.getenv("JSEARCH_API_KEY", "").strip())


def _first(row: dict[str, Any], keys: list[str], default: str = "") -> str:
    for key in keys:
        value = row.get(key)
        if value is not None and value != "":
            return str(value)
    return default


def _extract_rows(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if not isinstance(payload, dict):
        return []

    for key in ["data", "jobs", "results", "items", "job_results", "search_results", "organic_results"]:
        value = payload.get(key)
        if isinstance(value, list):
            return [x for x in value if isinstance(x, dict)]
        if isinstance(value, dict):
            nested = _extract_rows(value)
            if nested:
                return nested

    for value in payload.values():
        if isinstance(value, list) and value and all(isinstance(x, dict) for x in value[:3]):
            return [x for x in value if isinstance(x, dict)]
        if isinstance(value, dict):
            nested = _extract_rows(value)
            if nested:
                return nested
    return []


def _build_query(base_query: str, loc: str) -> str:
    base = (base_query or "").strip()
    location = (loc or "Malaysia").strip()
    lower = base.lower()

    if location.lower() == "malaysia":
        return base if "malaysia" in lower else f"{base} in Malaysia"

    if lower.endswith(" in malaysia"):
        base = base[: -len(" in malaysia")].strip()
    elif lower.endswith(" malaysia"):
        base = base[: -len(" malaysia")].strip()
    if location.lower() in base.lower():
        return base if "malaysia" in base.lower() else f"{base}, Malaysia"
    return f"{base} in {location}, Malaysia"


def _flatten_pairs(config: dict[str, Any]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for item in config.get("queries", []):
        base_query = item.get("query", "")
        for loc in item.get("locations", ["Malaysia"]):
            pairs.append((base_query, loc))
    return pairs


def _rotation_offset(total_pairs: int, max_requests: int) -> int:
    if total_pairs <= 0 or max_requests <= 0:
        return 0
    rotate = os.getenv("JSEARCH_ROTATE_QUERIES", "1").strip().lower()
    if rotate in {"0", "false", "no", "off"}:
        return 0

    run_number = os.getenv("GITHUB_RUN_NUMBER", "").strip()
    if run_number.isdigit():
        return ((int(run_number) - 1) * max_requests) % total_pairs

    now = datetime.now(timezone.utc)
    half_day_slot = 0 if now.hour < 12 else 1
    slot = now.toordinal() * 2 + half_day_slot
    return (slot * max_requests) % total_pairs


def _rotated_pairs(pairs: list[tuple[str, str]], max_requests: int) -> list[tuple[str, str]]:
    if not pairs:
        return pairs
    offset = _rotation_offset(len(pairs), max_requests)
    return pairs[offset:] + pairs[:offset]


def fetch(config: dict[str, Any], per_query: int = 10) -> list[JobPosting]:
    api_key = os.getenv("JSEARCH_API_KEY", "").strip()
    if not api_key:
        return []

    max_requests = int(os.getenv("JSEARCH_MAX_REQUESTS_PER_RUN", "3") or 3)
    request_count = 0

    jobs: list[JobPosting] = []
    headers = {"x-api-key": api_key}
    pairs = _rotated_pairs(_flatten_pairs(config), max_requests)

    print(f"[jsearch] query pairs available: {len(pairs)}; max requests this run: {max_requests}")

    for base_query, loc in pairs:
        if max_requests and request_count >= max_requests:
            print(f"[jsearch] request cap reached: {request_count}/{max_requests}")
            return jobs

        query = _build_query(base_query, loc)
        params = {
            "query": query,
            "country": "my",
            "language": "en",
            "page": "1",
            "num_pages": "1",
        }

        try:
            print(f"[jsearch] query: {query}")
            response = requests.get(API_URL, params=params, headers=headers, timeout=30)
            request_count += 1
            response.raise_for_status()
            payload = response.json()
        except Exception as exc:
            print(f"[jsearch] query failed: {query}: {exc}")
            continue

        rows = _extract_rows(payload)
        if not rows:
            if isinstance(payload, dict):
                print(f"[jsearch] no rows parsed for query: {query}; response keys: {list(payload.keys())}")
            else:
                print(f"[jsearch] no rows parsed for query: {query}; response type: {type(payload).__name__}")
            continue

        for row in rows[:per_query]:
            title = _first(row, ["job_title", "title", "position", "name"])
            company = _first(row, ["employer_name", "company_name", "company", "employer"])
            city = _first(row, ["job_city", "city"])
            state = _first(row, ["job_state", "state", "region"])
            location = _first(row, ["job_location", "location", "formatted_location"], loc)
            if not location and (city or state):
                location = ", ".join(x for x in [city, state, "Malaysia"] if x)

            desc = _first(row, ["job_description", "description", "snippet", "summary"])
            apply_url = _first(row, [
                "job_apply_link", "apply_link", "apply_url", "job_apply_url",
                "job_publisher_link", "job_google_link", "url", "link",
            ])
            source_url = _first(row, ["job_google_link", "job_publisher_link", "source_url", "url", "link"], apply_url)
            posted_at = _first(row, ["job_posted_at_datetime_utc", "job_posted_at_timestamp", "posted_at", "created_at", "date"])

            salary = ""
            if row.get("job_min_salary") or row.get("job_max_salary"):
                salary = f"{row.get('job_min_salary') or ''}-{row.get('job_max_salary') or ''} {row.get('job_salary_period') or ''}".strip()

            jobs.append(JobPosting(
                source="jsearch",
                title=title,
                company=company,
                location=str(location or loc or "Malaysia"),
                description=desc,
                apply_url=str(apply_url or ""),
                source_url=str(source_url or apply_url or ""),
                posted_at=str(posted_at or ""),
                salary=salary,
                raw=row,
            ))

    print(f"[jsearch] fetched {len(jobs)} jobs using {request_count} requests")
    return jobs
