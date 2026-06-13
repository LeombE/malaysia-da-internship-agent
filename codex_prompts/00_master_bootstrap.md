# Prompt 00 — Master Bootstrap for Codex

You are working in my GitHub repository for the Malaysia Data Analyst Internship Finder.

Use the repository instructions in `AGENTS.md` and the skill `malaysia-da-internship-agent` if available.

Context:
- My goal is to secure a Malaysia Data Analyst / Data Analytics / BI / SQL / Power BI / Business Analyst / Data Science internship.
- Target internship window is 2026-08-02 to 2026-11-03, about 3 months. Longer internships are acceptable if they can cover or align with this academic period.
- Priority locations: Johor, Selangor, Kuala Lumpur, Penang, then Malaysia-wide.
- Big companies should be prioritized, but the practical goal is offer probability, so SMEs and mass-apply roles must not be discarded.
- Salary is low priority.
- Current architecture: Python, SQLite, CSV outputs, JSearch API, GitHub Actions twice daily, GitHub Secrets.
- Current outputs: `data/latest_ranked_jobs.csv`, `data/today_shortlist.csv`, `data/internship_tracker.csv`, `data/jobs.db`.
- Current request cap may be `JSEARCH_MAX_REQUESTS_PER_RUN=3` to stay within OpenWeb Ninja Basic quota.

Your task:
1. Inspect the repository structure and key files.
2. Summarize the current project status.
3. Identify the top 5 risks or improvement opportunities.
4. Do not edit code yet.
5. Propose a safe next-step plan with validation commands.
6. Explicitly confirm that `.env` and `.venv` must never be committed.
7. If you need agents, spawn specialized subagents for recruitment quality, source integration, scoring, DevOps, and security review, then consolidate results.

Do not ask me to paste API keys. If secrets are needed, instruct me to add them through GitHub Secrets.
