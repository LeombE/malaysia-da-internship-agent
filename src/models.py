from __future__ import annotations

from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Any
import hashlib
import re


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def stable_hash(*parts: str | None) -> str:
    raw = "|".join((p or "").strip().lower() for p in parts)
    raw = re.sub(r"\s+", " ", raw)
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
        if not self.job_id:
            self.job_id = stable_hash(self.source, self.title, self.company, self.location, self.apply_url)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["reasons"] = "; ".join(self.reasons)
        return data
