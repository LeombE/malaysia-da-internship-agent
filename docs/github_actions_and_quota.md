# GitHub Actions and Quota Guide

This project runs automatically through GitHub Actions and uses OpenWeb Ninja JSearch quota during collection runs.

## Current GitHub Actions Schedule

The workflow is defined in `.github/workflows/daily.yml`.

Current UTC cron:

```yaml
cron: "30 4,10,15,22 * * *"
```

Malaysia time:

| UTC run | Malaysia time |
|---|---|
| 04:30 UTC | 12:30 MYT |
| 10:30 UTC | 18:30 MYT |
| 15:30 UTC | 23:30 MYT |
| 22:30 UTC | 06:30 MYT next day |

## Campaign Run Frequency

During the urgent 15-day campaign:

- GitHub Actions runs 4 times per day.
- `JSEARCH_MAX_REQUESTS_PER_RUN` is set to `160`.
- Each run rotates through the expanded query pool instead of searching the same first queries every time.
- The workflow exports CSV and SQLite outputs back to the repository.

## 15-Day Request Budget

Budget calculation:

```text
4 runs/day * 160 requests/run * 15 days = 9,600 automated requests
```

With a 10,000 requests/month plan, this leaves about 400 requests for manual validation and debugging.

The campaign is designed to improve practical internship discovery, not simply collect more rows. The expanded query strategy covers:

- Core Data Internship
- BI / SQL / Reporting
- Business / Operations Analytics
- Malay / Local Internship Terms
- Tier A Company Targeted
- Tier B / MNC / Manufacturing
- Malaysia-wide backup

## Required GitHub Secrets

Required for the current campaign:

| Secret | Purpose |
|---|---|
| `JSEARCH_API_KEY` | OpenWeb Ninja JSearch API authentication. |
| `JSEARCH_MAX_REQUESTS_PER_RUN` | Request cap. Set to `160` during the urgent campaign. |

Optional:

| Secret | Purpose |
|---|---|
| `ADZUNA_APP_ID` | Optional Adzuna API app ID. |
| `ADZUNA_APP_KEY` | Optional Adzuna API app key. |
| `GOOGLE_ALERT_FEEDS` | Optional comma-separated Google Alerts RSS feeds. |
| `TELEGRAM_BOT_TOKEN` | Optional Telegram notification bot token. |
| `TELEGRAM_CHAT_ID` | Optional Telegram chat ID. |
| `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `EMAIL_TO`, `EMAIL_FROM` | Optional email notifications. |

Never commit secret values. Documentation should mention secret names only.

## Manual Run Steps

Use manual runs only when quota usage is intended.

GitHub:

1. Open the repository on GitHub.
2. Go to Actions.
3. Select the Malaysia DA Internship Finder workflow.
4. Click Run workflow.
5. After completion, inspect generated CSV outputs.

Local:

```bash
python -m src.main --dry-run
```

Only run locally when the JSearch quota impact is acceptable.

## What to Check After a Run

After each GitHub Actions run, inspect:

| File | Check |
|---|---|
| `data/today_shortlist.csv` | Apply to `A_APPLY_NOW`, verify `B_APPLY_SOON`, mass apply useful `C_MASS_APPLY`. |
| `data/latest_ranked_jobs.csv` | Audit source quality, duplicates, false positives, and state coverage. |
| `data/internship_tracker.csv` | Preserve and update application status, follow-up dates, interview dates, and notes. |
| GitHub Actions log | Confirm request cap, run success, exported CSVs, and data commit. |

Campaign health metrics:

- New rows since last run.
- Bucket counts.
- State coverage.
- Official/ATS share.
- Aggregator share.
- Duplicate or wrong-intake rows.
- Tracker application outcomes.

## How to Reduce Quota After the Campaign

After the 15-day urgent campaign:

1. Reduce GitHub Secret `JSEARCH_MAX_REQUESTS_PER_RUN` from `160`.
2. Recommended values:
   - `60` for a moderate active search.
   - `30` or lower for maintenance mode.
   - `3` for emergency quota conservation.
3. Confirm `config.yml` campaign guard has rolled back or been updated.
4. Keep the GitHub Actions schedule only if the campaign is still needed.
5. Review source quality before increasing quota again.

## Safety Notes

- Do not print API keys or tokens in logs.
- Do not commit `.env` or `.venv/`.
- Do not add login scraping, CAPTCHA bypassing, paywall bypassing, or platform ToS-bypassing behavior.
- Prefer official APIs, public RSS feeds, official career pages, and public ATS links.
