from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse
import re

from .models import JobPosting


def _norm(value: str | None) -> str:
    return re.sub(r"\s+", " ", (value or "").strip().lower())


def _text(job: JobPosting) -> str:
    return _norm(" ".join([
        job.title or "",
        job.company or "",
        job.location or "",
        job.state or "",
        job.description or "",
        job.apply_url or "",
        job.source_url or "",
    ]))


def _contains_any(text: str, terms: list[str]) -> list[str]:
    found: list[str] = []
    for term in terms:
        t = _norm(term)
        if t and t in text:
            found.append(term)
    return found


def _regex_any(text: str, patterns: list[str]) -> list[str]:
    found: list[str] = []
    for pattern in patterns:
        if re.search(pattern, text, flags=re.I):
            found.append(pattern)
    return found


def normalize_state(location: str, preferred_states: list[str] | None = None) -> str:
    loc = _norm(location)
    aliases = [
        ("johor bahru", "Johor"),
        ("iskandar puteri", "Johor"),
        ("nusajaya", "Johor"),
        ("pasir gudang", "Johor"),
        ("senai", "Johor"),
        ("kulai", "Johor"),
        ("johor", "Johor"),
        ("petaling jaya", "Selangor"),
        ("subang jaya", "Selangor"),
        ("shah alam", "Selangor"),
        ("puchong", "Selangor"),
        ("cyberjaya", "Selangor"),
        ("klang", "Selangor"),
        ("kuala selangor", "Selangor"),
        ("selangor", "Selangor"),
        ("bangsar south", "Kuala Lumpur"),
        ("kuala lumpur", "Kuala Lumpur"),
        ("wilayah persekutuan", "Kuala Lumpur"),
        ("federal territory", "Kuala Lumpur"),
        (" kl ", "Kuala Lumpur"),
        ("bayan lepas", "Penang"),
        ("george town", "Penang"),
        ("bukit mertajam", "Penang"),
        ("pulau pinang", "Penang"),
        ("penang", "Penang"),
    ]
    padded = f" {loc} "
    for key, state in aliases:
        if key in padded or key in loc:
            return state
    for state in preferred_states or []:
        if _norm(state) in loc:
            return state
    if "malaysia" in loc:
        return "Malaysia"
    return ""


def _url_host(url: str) -> str:
    try:
        return _norm(urlparse(url).netloc.replace("www.", ""))
    except Exception:
        return ""


def _company_tier_score(company: str, config: dict[str, Any]) -> tuple[int, list[str]]:
    company_l = _norm(company)
    reasons: list[str] = []
    if not company_l or company_l in {"undisclosed", "confidential", "private advertiser"}:
        return -8, ["company undisclosed/confidential"]

    tiers = config.get("company_tiers", {})
    tier_1 = [_norm(c) for c in tiers.get("tier_1", [])]
    tier_2 = [_norm(c) for c in tiers.get("tier_2", [])]

    if any(c and (c in company_l or company_l in c) for c in tier_1):
        return 12, ["Tier-1 target company"]
    if any(c and (c in company_l or company_l in c) for c in tier_2):
        return 8, ["Tier-2 established company"]
    return 4, ["small/unknown company kept for mass-apply strategy"]


def _freshness_score(posted_at: str) -> tuple[int, list[str]]:
    if not posted_at:
        return 1, ["posting date unknown"]
    try:
        if str(posted_at).isdigit():
            dt = datetime.fromtimestamp(int(posted_at), tz=timezone.utc)
        else:
            dt = datetime.fromisoformat(str(posted_at).replace("Z", "+00:00"))
        days = (datetime.now(timezone.utc) - dt.astimezone(timezone.utc)).days
        if days <= 3:
            return 5, ["posted within 3 days"]
        if days <= 14:
            return 4, ["posted within 14 days"]
        if days <= 45:
            return 2, ["posted within 45 days"]
        return 0, ["older posting"]
    except Exception:
        return 1, ["posting date parse failed"]


def _source_quality_score(job: JobPosting, config: dict[str, Any]) -> tuple[int, list[str]]:
    reasons: list[str] = []
    score = 0
    url = job.apply_url or job.source_url or ""
    host = _url_host(url)
    full_url = _norm(url)
    sq = config.get("source_quality", {})

    if job.apply_url:
        score += 4
        reasons.append("has apply link")
    else:
        score -= 8
        reasons.append("missing apply link")

    official = [_norm(x) for x in sq.get("official_or_ats_domains", [])]
    trusted = [_norm(x) for x in sq.get("trusted_job_boards", [])]
    low_signal = [_norm(x) for x in sq.get("aggregator_or_low_signal", [])]

    if any(x and x in full_url for x in official):
        score += 10
        reasons.append("official/ATS source likely higher reliability")
    elif any(x and x in full_url for x in trusted):
        score += 5
        reasons.append("trusted job board source")
    elif any(x and x in full_url for x in low_signal):
        score -= 8
        reasons.append("aggregator/low-signal source; manually verify before applying")
    elif host:
        score += 1
        reasons.append(f"source host: {host}")

    return max(-12, min(12, score)), reasons


def _location_score(job: JobPosting, text: str, config: dict[str, Any]) -> tuple[int, list[str]]:
    target = config.get("target", {})
    state = job.state or normalize_state(" ".join([job.location, job.state, text]), target.get("preferred_states", []))
    job.state = state
    weights = target.get("location_weights", {})
    reasons: list[str] = []
    score = 0

    if state in weights:
        score += int(weights[state])
        reasons.append(f"location priority: {state}")
    elif "remote" in text or "anywhere" in text:
        score += 6
        reasons.append("remote/anywhere role, verify Malaysia eligibility")
    elif "malaysia" in text:
        score += int(weights.get("Malaysia", 6))
        reasons.append("Malaysia-wide role")
    else:
        score -= 10
        reasons.append("location not clearly Malaysia or priority states")

    city_weights = target.get("preferred_cities", {})
    if isinstance(city_weights, dict):
        matched = []
        for city, weight in city_weights.items():
            if _norm(city) in text:
                score += int(weight)
                matched.append(city)
        if matched:
            reasons.append("priority city: " + ", ".join(matched[:3]))

    return max(-10, min(18, score)), reasons


def _role_score(text: str, config: dict[str, Any]) -> tuple[int, list[str]]:
    kw = config.get("keywords", {})
    reasons: list[str] = []
    score = 0

    internship = _contains_any(text, kw.get("internship", []))
    core = _contains_any(text, kw.get("role_core", []))
    adjacent = _contains_any(text, kw.get("role_adjacent", []))
    skills = _contains_any(text, kw.get("skills", []))

    if internship:
        score += 10
        reasons.append("internship/practical training role")
    if core:
        score += min(12, 5 * len(core))
        reasons.append("core role keyword: " + ", ".join(core[:3]))
    elif adjacent:
        score += min(7, 3 * len(adjacent))
        reasons.append("adjacent analytics role keyword: " + ", ".join(adjacent[:3]))
    if skills:
        score += min(6, 2 * len(skills))
        reasons.append("analytics skill match: " + ", ".join(skills[:4]))

    if not internship:
        score -= 10
        reasons.append("not clearly internship; lower priority")
    if not core and not adjacent:
        score -= 8
        reasons.append("not clearly data/analytics role")

    return max(-18, min(28, score)), reasons


def _window_score(text: str, config: dict[str, Any]) -> tuple[int, list[str]]:
    kw = config.get("keywords", {})
    reasons: list[str] = []
    score = 0

    duration = _contains_any(text, kw.get("duration_fit", []))
    date_window = _contains_any(text, kw.get("date_window", []))

    if duration:
        score += 8
        reasons.append("duration likely fits 3-month industrial training")
    if date_window:
        score += 8
        reasons.append("mentions Aug-Nov 2026 target window")
    if re.search(r"\b6\s*months?\b|six\s*months?", text):
        score += 2
        reasons.append("longer internship may still be acceptable")
    if "summer 2026" in text:
        score += 1
        reasons.append("Summer 2026 mention; verify if it can cover Aug-Nov requirement")

    # Most Malaysian postings do not mention exact intake months. Avoid over-penalizing unknown dates.
    if not duration and not date_window:
        score += 3
        reasons.append("date not stated; keep for manual confirmation")

    return min(16, score), reasons


def _requirement_score(text: str, config: dict[str, Any]) -> tuple[int, list[str]]:
    kw = config.get("keywords", {})
    reasons: list[str] = []
    score = 0
    student = _contains_any(text, kw.get("student_fit", []))
    skills = _contains_any(text, kw.get("skills", []))
    if student:
        score += 4
        reasons.append("student/entry-level friendly")
    if skills:
        score += min(3, len(skills))
        reasons.append("resume skill fit: " + ", ".join(skills[:3]))
    return min(7, score), reasons


def _penalties(job: JobPosting, text: str, config: dict[str, Any]) -> tuple[int, list[str]]:
    kw = config.get("keywords", {})
    reasons: list[str] = []
    penalty = 0

    hard_patterns = [
        r"\bsenior\b",
        r"\bmanager\b",
        r"\bdirector\b",
        r"\bhead of\b",
        r"\bpermanent\b",
        r"\b[3-9]\+?\s+years?\b",
        r"\b[3-9]\s+years?\s+experience\b",
    ]
    matches = _regex_any(text, hard_patterns)
    if matches:
        penalty += min(28, 7 * len(matches))
        reasons.append("seniority/permanent/experience red flag")

    neg = _contains_any(text, kw.get("negative", []))
    if neg:
        penalty += min(18, 4 * len(neg))
        reasons.append("negative keyword: " + ", ".join(neg[:5]))

    non_my = _contains_any(text, kw.get("non_malaysia_noise", []))
    if non_my and not job.state:
        penalty += 25
        reasons.append("non-Malaysia location noise")
    elif non_my:
        penalty += 8
        reasons.append("possible non-Malaysia noise; verify manually")

    if "master" in text or "masters" in text:
        penalty += 4
        reasons.append("may target Masters-level candidate")

    if ("sales" in text or "telemarketing" in text) and "data analyst" not in text and "analytics" not in text:
        penalty += 12
        reasons.append("sales-heavy role, likely weak data fit")

    return penalty, reasons


def _bucket(score: int) -> str:
    if score >= 70:
        return "A_APPLY_NOW"
    if score >= 55:
        return "B_APPLY_SOON"
    if score >= 42:
        return "C_MASS_APPLY"
    return "D_LOW_PRIORITY"


def score_job(job: JobPosting, config: dict[str, Any]) -> JobPosting:
    text = _text(job)
    reasons: list[str] = []
    score = 0

    for value, rs in [
        _role_score(text, config),
        _location_score(job, text, config),
        _window_score(text, config),
        _company_tier_score(job.company, config),
        _source_quality_score(job, config),
        _requirement_score(text, config),
        _freshness_score(job.posted_at),
    ]:
        score += value
        reasons.extend(rs)

    penalty, penalty_reasons = _penalties(job, text, config)
    score -= penalty
    reasons.extend(penalty_reasons)

    final_score = max(0, min(100, int(score)))
    job.score = final_score
    job.reasons = [f"bucket: {_bucket(final_score)}"] + reasons
    return job
