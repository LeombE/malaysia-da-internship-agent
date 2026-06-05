from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import re

from .models import JobPosting


def _text(job: JobPosting) -> str:
    return " ".join([
        job.title or "",
        job.company or "",
        job.location or "",
        job.state or "",
        job.description or "",
    ]).lower()


def _contains_any(text: str, terms: list[str]) -> list[str]:
    found = []
    for term in terms:
        if term.lower() in text:
            found.append(term)
    return found


def normalize_state(location: str, preferred_states: list[str]) -> str:
    loc = (location or "").lower()
    aliases = {
        "kl": "Kuala Lumpur",
        "kuala lumpur": "Kuala Lumpur",
        "wilayah persekutuan": "Kuala Lumpur",
        "selangor": "Selangor",
        "petaling jaya": "Selangor",
        "pj": "Selangor",
        "subang": "Selangor",
        "shah alam": "Selangor",
        "cyberjaya": "Selangor",
        "johor": "Johor",
        "johor bahru": "Johor",
        "iskandar": "Johor",
        "senai": "Johor",
        "penang": "Penang",
        "pulau pinang": "Penang",
        "bayan lepas": "Penang",
        "george town": "Penang",
    }
    for key, state in aliases.items():
        if key in loc:
            return state
    for state in preferred_states:
        if state.lower() in loc:
            return state
    return ""


def _date_fit_score(text: str) -> tuple[int, list[str]]:
    reasons: list[str] = []
    score = 0

    duration_patterns = [
        r"\b3\s*months?\b",
        r"\bthree\s*months?\b",
        r"\b3\s*[-–]\s*6\s*months?\b",
        r"minimum\s+3\s*months?",
        r"at\s+least\s+3\s*months?",
        r"latihan\s+industri",
        r"industrial\s+training",
    ]
    long_duration_patterns = [r"\b6\s*months?\b", r"six\s*months?", r"\b12\s*months?\b"]
    date_patterns = [
        r"aug(?:ust)?\s*2026",
        r"sep(?:tember)?\s*2026",
        r"oct(?:ober)?\s*2026",
        r"nov(?:ember)?\s*2026",
        r"2026[-/]0?8",
        r"2026[-/]0?9",
        r"2026[-/]10",
        r"2026[-/]11",
    ]

    if any(re.search(p, text) for p in duration_patterns):
        score += 11
        reasons.append("duration likely matches 3-month internship")
    if any(re.search(p, text) for p in date_patterns):
        score += 9
        reasons.append("mentions Aug-Nov 2026 window")
    if any(re.search(p, text) for p in long_duration_patterns):
        score += 5
        reasons.append("longer internship may still be acceptable")
    if "intern" in text or "internship" in text or "praktikal" in text:
        score += 3
    return min(score, 20), reasons


def _company_tier_score(company: str, config: dict[str, Any]) -> tuple[int, str]:
    company_l = (company or "").lower()
    tier_1 = [c.lower() for c in config.get("company_tiers", {}).get("tier_1", [])]
    tier_2 = [c.lower() for c in config.get("company_tiers", {}).get("tier_2", [])]
    if any(c in company_l or company_l in c for c in tier_1 if c):
        return 15, "Tier-1 target company"
    if any(c in company_l or company_l in c for c in tier_2 if c):
        return 10, "Tier-2 established company"
    return 4, "company not in target list"


def _freshness_score(posted_at: str) -> tuple[int, str]:
    if not posted_at:
        return 3, "posting date unknown"
    try:
        dt = datetime.fromisoformat(posted_at.replace("Z", "+00:00"))
        days = (datetime.now(timezone.utc) - dt.astimezone(timezone.utc)).days
        if days <= 3:
            return 10, "posted within 3 days"
        if days <= 14:
            return 7, "posted within 14 days"
        if days <= 45:
            return 4, "posted within 45 days"
        return 1, "older posting"
    except Exception:
        return 3, "posting date parse failed"


def score_job(job: JobPosting, config: dict[str, Any]) -> JobPosting:
    text = _text(job)
    reasons: list[str] = []
    score = 0

    positive = config.get("keywords", {}).get("positive", [])
    skills = config.get("keywords", {}).get("skills", [])
    negative = config.get("keywords", {}).get("negative", [])
    preferred_states = config.get("target", {}).get("preferred_states", [])
    preferred_cities = config.get("target", {}).get("preferred_cities", [])

    # Role fit, max 30
    role_score = 0
    if "intern" in text or "internship" in text or "praktikal" in text or "latihan industri" in text:
        role_score += 12
        reasons.append("internship/practical training role")
    found_positive = _contains_any(text, positive)
    if found_positive:
        role_score += min(12, 4 * len(found_positive))
        reasons.append("role keyword: " + ", ".join(found_positive[:3]))
    found_skills = _contains_any(text, skills)
    if found_skills:
        role_score += min(6, 2 * len(found_skills))
        reasons.append("analytics skill match: " + ", ".join(found_skills[:4]))
    score += min(role_score, 30)

    # Date fit, max 20
    date_score, date_reasons = _date_fit_score(text)
    score += date_score
    reasons.extend(date_reasons)

    # Location fit, max 15
    state = job.state or normalize_state(job.location, preferred_states)
    job.state = state
    if state in preferred_states:
        score += 12
        reasons.append(f"preferred state: {state}")
    elif "malaysia" in text:
        score += 6
        reasons.append("Malaysia-wide role")
    if any(city.lower() in text for city in preferred_cities):
        score += 3
        reasons.append("preferred city match")

    # Company tier, max 15
    company_score, company_reason = _company_tier_score(job.company, config)
    score += company_score
    reasons.append(company_reason)

    # Freshness, max 10
    freshness_score, freshness_reason = _freshness_score(job.posted_at)
    score += freshness_score
    reasons.append(freshness_reason)

    # Requirement fit, max 10
    if any(term in text for term in ["entry level", "student", "undergraduate", "fresh graduate", "no experience", "diploma", "degree"]):
        score += 5
        reasons.append("student/entry-level friendly")
    if any(term in text for term in ["apply", "application", "career", "job", "vacancy"]):
        score += 2
    if job.apply_url:
        score += 3
        reasons.append("has apply link")

    # Penalties
    found_negative = _contains_any(text, negative)
    if found_negative:
        penalty = min(25, 5 * len(found_negative))
        score -= penalty
        reasons.append("penalty keywords: " + ", ".join(found_negative[:5]))
    if "intern" not in text and "praktikal" not in text and "latihan industri" not in text:
        score -= 8
        reasons.append("not clearly an internship")

    job.score = max(0, min(100, score))
    job.reasons = reasons
    return job
