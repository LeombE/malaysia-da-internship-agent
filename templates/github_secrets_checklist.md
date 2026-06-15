# GitHub Secrets Checklist

Use GitHub repository secrets for production automation.

Path:

`GitHub repo -> Settings -> Secrets and variables -> Actions -> New repository secret`

## Required During the 15-Day Campaign

- `JSEARCH_API_KEY`: OpenWeb Ninja JSearch API key. Paste the key only. Do not include quotes. Do not include `JSEARCH_API_KEY=`.
- `JSEARCH_MAX_REQUESTS_PER_RUN`: set to `160` during the 15-day urgent campaign.

Campaign budget:

- 4 GitHub Actions runs per day.
- 160 JSearch requests per run.
- 15 days uses about `4 * 160 * 15 = 9,600` automated requests.
- About 400 requests remain from a 10,000/month plan for manual validation/debug.

## After the Campaign

Reduce `JSEARCH_MAX_REQUESTS_PER_RUN` after the 15-day campaign.

Recommended post-campaign values:

- `60` for a lighter but still active search mode.
- `30` or lower for maintenance mode.
- `3` for very low-quota or emergency conservation mode.

Also confirm `config.yml` campaign settings have rolled back or been updated for the next search period.

## Optional Source Secrets

- `ADZUNA_APP_ID`
- `ADZUNA_APP_KEY`
- `GOOGLE_ALERT_FEEDS`

## Optional Notification Secrets

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASS`
- `EMAIL_TO`
- `EMAIL_FROM`

## Repository Actions Setting

Path:

`Settings -> Actions -> General -> Workflow permissions`

Set workflow permissions to read and write if the workflow should commit generated data files back to the repository.

## Safety Rules

- Never commit `.env`.
- Never commit `.venv/`.
- Never paste API keys, Telegram tokens, SMTP passwords, or GitHub tokens into README files, issues, pull requests, or logs.
- Keep secret values only in local `.env` or GitHub Secrets.
- In documentation, mention secret names only.
- Before every commit, run `git status --short --branch` and verify `.env`, `.venv/`, and credentials are not staged.
