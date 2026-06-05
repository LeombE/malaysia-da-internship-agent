from __future__ import annotations

import os
import smtplib
import textwrap
from email.message import EmailMessage
from typing import Sequence

import requests


def format_jobs_message(jobs: Sequence[dict], title: str = "Malaysia Data Analyst Internship Digest") -> str:
    if not jobs:
        return f"{title}\n\nNo high-score new jobs found in this run."

    parts = [title, ""]
    for i, job in enumerate(jobs, 1):
        reasons = job.get("reasons", "")
        if len(reasons) > 220:
            reasons = reasons[:217] + "..."
        bucket = job.get("bucket", "")
        line = f"{i}. [{job.get('score')}] {bucket} | {job.get('title')} — {job.get('company')}"
        parts.append(line)
        parts.append(f"   Location: {job.get('location') or job.get('state') or 'Unknown'} | Source: {job.get('source')}")
        parts.append(f"   Action: {job.get('recommended_action', 'Review manually.')}")
        parts.append(f"   Why: {reasons}")
        url = job.get("apply_url") or job.get("source_url")
        if url:
            parts.append(f"   Apply: {url}")
        parts.append("")
    return "\n".join(parts)


def send_telegram(message: str) -> bool:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        return False

    chunks = textwrap.wrap(message, width=3500, replace_whitespace=False, drop_whitespace=False)
    if not chunks:
        chunks = [message]
    for chunk in chunks:
        resp = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": chunk, "disable_web_page_preview": True},
            timeout=30,
        )
        resp.raise_for_status()
    return True


def send_email(subject: str, body: str) -> bool:
    host = os.getenv("SMTP_HOST", "").strip()
    port = int(os.getenv("SMTP_PORT", "587") or 587)
    user = os.getenv("SMTP_USER", "").strip()
    password = os.getenv("SMTP_PASS", "").strip()
    to_addr = os.getenv("EMAIL_TO", "").strip()
    from_addr = os.getenv("EMAIL_FROM", "").strip() or user
    if not host or not user or not password or not to_addr:
        return False

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg.set_content(body)

    with smtplib.SMTP(host, port, timeout=30) as server:
        server.starttls()
        server.login(user, password)
        server.send_message(msg)
    return True
