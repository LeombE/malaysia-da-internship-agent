from __future__ import annotations

from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Any
import hashlib
import re


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _clean(value: str | None) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"https?://\S+", "", value)
    value = re.sub(r"\b(internship|intern|trainee|practical training|industrial training)\b", "intern", value)
    value = re.sub(r"[^a-z0-9]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def stable_hash(*parts: str | None) -> str:
    raw = "|".join(_clean(p) for p in parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


@dataclass
class JobPosting:
    source: str
    title: str
    company: str
    location: str = ""
    state: str = ""
    description: str = ""
    apply_url: str = ""
    source_url: str = ""
    posted_at: str = ""
    salary: str = ""
    raw: dict[str, Any] = field(default_factory=dict)
    collected_at: str = field(default_factory=utc_now_iso)
    job_id: str = ""
    score: int = 0
    reasons: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        # V2: canonical ID ignores source/apply URL to reduce duplicate listings from aggregators.
        if not self.job_id:
            self.job_id = stable_hash(self.title, self.company, self.location or self.state)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["reasons"] = "; ".join(self.reasons)
        return data
