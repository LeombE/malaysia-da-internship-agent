# AGENTS.md — Malaysia Data Analyst Internship Agent

## Mission

Maintain and improve a Python + GitHub Actions project that automatically finds, ranks, stores, and summarizes Malaysia Data Analyst Internship opportunities for the user.

The practical goal is not merely to find famous companies. The practical goal is to maximize the user's probability of receiving and accepting a suitable internship offer for the academic requirement.

## User profile and constraints

- User is targeting a Data Analyst / Data Analytics / BI / Reporting / SQL / Power BI / Business Analyst / Data Science internship in Malaysia.
- Target internship period: 2026-08-02 to 2026-11-03, approximately 3 months.
- Internships longer than 3 months are acceptable if they can cover or align with the Aug-Nov 2026 academic window.
- Priority locations: Johor first, then Selangor, Kuala Lumpur, Penang, then Malaysia-wide fallback.
- Salary is low priority.
- Hireability is high priority.
- Big companies, MNCs, banks, Big 4, semiconductor/manufacturing analytics, telecommunications, e-commerce, and reputable tech companies should be prioritized, but SMEs must remain in the mass-apply pool because offer probability matters.
- User is willing to apply broadly and wants an automated, reliable, quota-aware pipeline.

## Current architecture

- Language: Python.
- Local OS used by user: Windows CMD.
- Main command: `python -m src.main --dry-run` for local test.
- GitHub Actions workflow: `.github/workflows/daily.yml`.
- Main data source: OpenWeb Ninja JSearch API through `JSEARCH_API_KEY`.
- Request cap: `JSEARCH_MAX_REQUESTS_PER_RUN`, currently 3 for free 200 requests/month quota.
- Schedule: daily twice, 08:30 and 20:30 Malaysia time, implemented as UTC cron in GitHub Actions.
- Outputs:
  - `data/latest_ranked_jobs.csv`
  - `data/today_shortlist.csv`
  - `data/internship_tracker.csv`
  - `data/jobs.db`

## Non-negotiable safety rules

- Never print, commit, log, or expose API keys, Telegram tokens, email passwords, GitHub tokens, or any secrets.
- Never commit `.env` or `.venv`.
- Verify `git status` before every commit.
- Use GitHub Secrets for secrets: `JSEARCH_API_KEY`, `JSEARCH_MAX_REQUESTS_PER_RUN`, and future notification/API tokens.
- Do not implement scraping that bypasses login, CAPTCHA, paywalls, robots.txt, or platform terms.
- Do not automate LinkedIn or Jobstreet login/scraping. Prefer APIs, RSS/Atom, Google Alerts RSS, public company career pages, and official ATS links.
- Treat aggregator websites as lower-confidence sources, not forbidden sources.
- Use official application links whenever possible.
- Make small, reviewable commits.
- Preserve user-editable tracker fields when modifying `data/internship_tracker.csv`.

## Scoring principles

The system should score based on:

1. Internship fit and hireability.
2. Location fit: Johor, Selangor, KL, Penang, Malaysia.
3. Role fit: Data Analyst, Data Analytics, BI, Reporting, SQL, Power BI, Data Science, Business Analyst.
4. Date/duration fit: Aug-Nov 2026, 3 months, industrial training, practical training, internship intake.
5. Company quality: big company/MNC/recognized firm receives bonus.
6. Source quality: official career page and ATS receive bonus; aggregators receive modest penalty.
7. Noise penalties: senior, manager, permanent, full-time non-internship, country mismatch, 3+ years required, undisclosed company.

Buckets:

- `A_APPLY_NOW`: apply today.
- `B_APPLY_SOON`: apply within 48 hours after quick verification.
- `C_MASS_APPLY`: lower certainty but useful for high-volume applications.
- `D_LOW_PRIORITY`: keep for record but usually ignore.

## Standard validation commands

On Windows CMD from repo root:

```cmd
.venv\Scripts\activate.bat
python -m src.main --dry-run
git status
```

For quota-safe test:

```cmd
set JSEARCH_MAX_REQUESTS_PER_RUN=1
python -m src.main --dry-run
set JSEARCH_MAX_REQUESTS_PER_RUN=
```

Before pushing:

```cmd
git status
git add .
git status
git commit -m "<clear message>"
git push
```

After pushing, verify GitHub Actions success and inspect generated CSV files.

## When asked to improve the project

First inspect:

- `config.yml`
- `src/main.py`
- `src/scoring.py`
- `src/sources/jsearch.py`
- `src/storage.py`
- `src/models.py`
- `src/notifications.py`
- `.github/workflows/daily.yml`
- `data/latest_ranked_jobs.csv`
- `data/today_shortlist.csv`
- `data/internship_tracker.csv`

Then propose a short plan before editing. Do not rewrite the entire project unless necessary.

## Preferred next roadmap

V3 should prioritize:

1. Telegram notification for `A_APPLY_NOW` and high-confidence `B_APPLY_SOON` roles.
2. Deduplication that prefers official/ATS links over aggregators.
3. Official career page / ATS boost.
4. Aggregator penalty that does not delete useful SME opportunities.
5. Application tracker preservation and better application status workflow.
6. Google Alerts RSS and Adzuna integration if quota and quality justify it.
7. Company career-page monitors for top firms in Malaysia.
