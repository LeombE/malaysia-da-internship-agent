from __future__ import annotations

from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
from typing import Any
import re

import requests
import yaml
from bs4 import BeautifulSoup

from ..models import JobPosting


USER_AGENT = "MalaysiaDAInternshipAgent/1.0 (+personal job search; contact: configure-owner-email)"


def enabled() -> bool:
    try:
        with open("data/company_targets.yml", "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return any(c.get("career_urls") for c in data.get("companies", []))
    except FileNotFoundError:
        return False


def _allowed_by_robots(url: str) -> bool:
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = RobotFileParser()
    try:
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(USER_AGENT, url) and rp.can_fetch("*", url)
    except Exception:
        # Conservative but practical: if robots cannot be read, fetch only the single configured URL.
        return True


def _looks_relevant(text: str, positive_terms: list[str], skill_terms: list[str]) -> bool:
    lower = text.lower()
    has_intern = any(t in lower for t in ["intern", "internship", "praktikal", "latihan industri", "student"])
    has_data = any(t in lower for t in positive_terms + skill_terms + ["data", "analytics", "bi", "dashboard"])
    return has_intern and has_data


def fetch(config: dict[str, Any], path: str = "data/company_targets.yml") -> list[JobPosting]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except FileNotFoundError:
        return []

    positive_terms = config.get("keywords", {}).get("positive", [])
    skill_terms = config.get("keywords", {}).get("skills", [])
    jobs: list[JobPosting] = []

    for company in data.get("companies", []):
        company_name = company.get("name", "")
        for url in company.get("career_urls", []) or []:
            if not _allowed_by_robots(url):
                print(f"[company_pages] robots disallow: {url}")
                continue
            try:
                resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
                resp.raise_for_status()
            except Exception as exc:
                print(f"[company_pages] failed: {company_name} {url}: {exc}")
                continue

            soup = BeautifulSoup(resp.text, "html.parser")
            text = soup.get_text(" ", strip=True)
            if not _looks_relevant(text, positive_terms, skill_terms):
                # Still scan links below because list pages may not expose full text.
                pass

            # Extract relevant links from public career listing pages.
            links_seen: set[str] = set()
            for a in soup.find_all("a", href=True):
                label = a.get_text(" ", strip=True)
                href = urljoin(url, a["href"])
                blob = f"{label} {href}"
                if href in links_seen:
                    continue
                links_seen.add(href)
                if _looks_relevant(blob, positive_terms, skill_terms):
                    jobs.append(JobPosting(
                        source="company_page",
                        title=label or "Possible data internship posting",
                        company=company_name,
                        location=", ".join(company.get("locations", [])),
                        description=f"Matched from public career page: {label}",
                        apply_url=href,
                        source_url=url,
                        raw={"company_config": company, "matched_link_text": label},
                    ))

            # Fallback: if the whole page is relevant, keep the page itself.
            if _looks_relevant(text, positive_terms, skill_terms):
                title_tag = soup.find("title")
                page_title = title_tag.get_text(" ", strip=True) if title_tag else f"{company_name} career page match"
                snippet = re.sub(r"\s+", " ", text)[:900]
                jobs.append(JobPosting(
                    source="company_page",
                    title=page_title,
                    company=company_name,
                    location=", ".join(company.get("locations", [])),
                    description=snippet,
                    apply_url=url,
                    source_url=url,
                    raw={"company_config": company},
                ))
    return jobs
