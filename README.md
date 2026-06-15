# Malaysia Data Analyst Internship Intelligence Pipeline

## 2-Minute Project Summary

This repository is a production-style data pipeline that helps a student find and prioritize Malaysia Data Analyst, Data Analytics, BI, Reporting, SQL, Power BI, Business Analyst, and Data Science internships for the target window of 2026-08-02 to 2026-11-03.

It collects internship leads from responsible job sources, cleans and normalizes the records, scores each role against business rules, stores results in SQLite, exports decision-ready CSV files, and runs automatically through GitHub Actions.

The project is built to prove practical Data Analyst internship skills:

- Python data ingestion and transformation
- API-based data collection
- Data cleaning and deduplication
- Business-rule scoring
- SQLite persistence
- CSV reporting
- GitHub Actions automation
- Stakeholder-focused decision support
- Responsible data sourcing and secret handling

## Stakeholder and Business Problem

The stakeholder is a student who needs a suitable Malaysia-based internship offer for an academic requirement. The practical business problem is not simply finding more job posts. It is deciding what to apply to first when job boards are noisy, duplicated, incomplete, and spread across many sources.

The system improves this decision:

> Which internship roles should the user apply to today, verify manually, mass apply to, or ignore?

The ranking prioritizes offer probability and internship fit over salary. Large companies, MNCs, banks, Big 4 firms, semiconductor/manufacturing analytics roles, telecommunications, e-commerce, and reputable technology companies are prioritized, while SME roles remain available for mass-apply coverage.

## Current Architecture and Workflow

```text
GitHub Actions schedule
        |
        v
src/main.py
        |
        +-- src/sources/jsearch.py          OpenWeb Ninja JSearch API
        +-- src/sources/adzuna.py           Optional Adzuna API
        +-- src/sources/google_alerts.py    Optional Google Alerts RSS
        +-- src/sources/company_pages.py    Optional public career pages
        |
        v
src/scoring.py       Role, location, date, company, source, and risk scoring
        |
        v
src/storage.py       SQLite upsert, deduplication, CSV exports, tracker preservation
        |
        v
data/jobs.db
data/latest_ranked_jobs.csv
data/today_shortlist.csv
data/internship_tracker.csv
```

The pipeline can run locally and in GitHub Actions. During the urgent 15-day campaign, GitHub Actions runs 4 times per day with `JSEARCH_MAX_REQUESTS_PER_RUN=160`.

## Data Sources and Responsible Sourcing

The main source is OpenWeb Ninja JSearch API. The project also includes optional integrations for Adzuna API, Google Alerts RSS, and public company career pages.

Responsible sourcing rules:

- Prefer official APIs, public RSS feeds, official career pages, and public ATS links.
- Do not automate login scraping.
- Do not bypass CAPTCHA, paywalls, robots.txt, or platform restrictions.
- Treat aggregators as lower-confidence sources, not forbidden sources.
- Prefer official company career pages and ATS links when duplicates exist.
- Never commit secrets or credentials.

## Output Files and How to Use Them

| File | Purpose | Stakeholder use |
|---|---|---|
| `data/latest_ranked_jobs.csv` | Full ranked job output | Review complete pipeline results and audit ranking quality. |
| `data/today_shortlist.csv` | Top actionable A/B/C shortlist | Decide what to apply to today. |
| `data/internship_tracker.csv` | Application tracking table | Record applied status, follow-up dates, interviews, offers, and notes. |
| `data/jobs.db` | SQLite job history | Preserve first seen, last seen, deduped records, and run history. |

See:

- `docs/data_dictionary.md`
- `docs/scoring_methodology.md`
- `reports/latest_campaign_summary.md`

## Scoring and Bucket Methodology

Each job is scored from 0 to 100 using practical business rules:

- Role relevance: Data Analyst, Data Analytics, BI, SQL, Power BI, Reporting, Business Analyst, Data Science.
- Internship fit: internship, practical training, industrial training, student-friendly language.
- Location fit: Johor, Selangor, Kuala Lumpur, Penang, Malaysia-wide fallback.
- Date and duration fit: Aug-Nov 2026, 3 months, 3-6 months, industrial training.
- Company quality: Tier 1 and Tier 2 target companies receive bonuses.
- Source quality: official/ATS sources receive bonuses, trusted job boards receive moderate bonuses, aggregator-only links receive a penalty.
- Risk penalties: senior, manager, permanent, non-Malaysia, high-experience, undisclosed company, or weak role fit.

Buckets:

| Bucket | Meaning | Action |
|---|---|---|
| `A_APPLY_NOW` | Highest-priority roles | Apply today after checking date and duration. |
| `B_APPLY_SOON` | Strong roles with some verification needed | Apply within 48 hours after quick manual review. |
| `C_MASS_APPLY` | Lower certainty but still useful | Use for broad application volume and SME coverage. |
| `D_LOW_PRIORITY` | Weak or noisy matches | Keep for record; usually ignore. |

## Current Measurable Results

Latest checked output snapshot as of `2026-06-14T23:59:52+00:00`.

These metrics are generated outputs and will change after scheduled GitHub Actions runs.

| Metric | Value |
|---|---:|
| Rows in `latest_ranked_jobs.csv` | 500 |
| Rows in `today_shortlist.csv` | 80 |
| Rows in `internship_tracker.csv` | 353 |
| Newest campaign rows in `latest_ranked_jobs.csv` | 420 |
| Newest `A_APPLY_NOW` rows | 10 |
| Newest `B_APPLY_SOON` rows | 61 |
| Newest `C_MASS_APPLY` rows | 226 |
| Newest `D_LOW_PRIORITY` rows | 123 |
| Newest Selangor rows | 154 |
| Newest Kuala Lumpur rows | 132 |
| Newest Penang rows | 82 |
| Newest Johor rows | 21 |
| Newest Malaysia-wide rows | 30 |
| Newest unclassified rows | 1 |

Example high-priority companies surfaced in the current outputs include Grab, TNG Digital, Maxis, DXC Technology, Infineon, Allianz, Abbott, AXA, PETRONAS-related roles, Bosch, Volvo Trucks, WPP Media, and Hilti.

## GitHub Actions Automation

The urgent campaign runs four times per day in Malaysia time:

- 06:30 MYT
- 12:30 MYT
- 18:30 MYT
- 23:30 MYT

GitHub Actions implements that schedule with this UTC cron:

```yaml
cron: "30 4,10,15,22 * * *"
```

Campaign quota strategy:

- 4 runs per day
- 160 JSearch requests per run
- 15-day target: about 9,600 automated requests
- Reserve: about 400 requests for manual validation/debug

After the campaign, reduce `JSEARCH_MAX_REQUESTS_PER_RUN` to 60 or lower.

## Security and Secrets Policy

Secrets are supplied through `.env` locally and GitHub Secrets in production. They must never be committed.

Important secret names:

- `JSEARCH_API_KEY`
- `JSEARCH_MAX_REQUESTS_PER_RUN`
- `ADZUNA_APP_ID`
- `ADZUNA_APP_KEY`
- `GOOGLE_ALERT_FEEDS`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- SMTP/email secrets if enabled

The repository ignores `.env`, `.venv/`, Python caches, and SQLite WAL/SHM files.

## Limitations and Known Data Quality Risks

- Aggregator sources can dominate output volume and may contain stale, duplicated, or rewritten listings.
- Some roles do not state the exact Aug-Nov 2026 internship window and need manual verification.
- Some listings mention wrong intake periods such as Jan-Apr 2026 or Summer 2026.
- Some location/state classification can be imperfect when the source text contains multiple city names or URLs.
- The tracker is only useful once application statuses are updated manually.
- The pipeline ranks evidence; it does not guarantee that a role is still open.

## Resume-Ready Bullets

- Built a Python and GitHub Actions data pipeline that collects, cleans, scores, ranks, and exports Malaysia internship leads from API and public data sources.
- Designed a business-rule scoring model that prioritizes internship fit, location fit, company quality, source reliability, and actionability.
- Automated a 15-day campaign running 4 times per day with 160 JSearch requests per run, targeting about 9,600 automated searches.
- Produced decision-ready CSV reports with action buckets: apply now, apply soon, mass apply, and low priority.
- Implemented SQLite persistence, deduplication, first/last seen tracking, and tracker field preservation for application follow-up.
- Applied responsible data sourcing practices by using APIs, RSS, public career pages, GitHub Secrets, and no login/CAPTCHA bypassing.

## Local Use

Windows CMD:

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run only when quota use is intended:

```cmd
python -m src.main --dry-run
```

For portfolio review, inspect the generated CSVs and Markdown docs instead of rerunning collection.
