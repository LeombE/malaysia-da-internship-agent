# GitHub Secrets Checklist

Go to:

`GitHub repo -> Settings -> Secrets and variables -> Actions -> New repository secret`

Required now:

- `JSEARCH_API_KEY`: OpenWeb Ninja JSearch API key. Paste the key only. No quotes. No `JSEARCH_API_KEY=` prefix.
- `JSEARCH_MAX_REQUESTS_PER_RUN`: `3` for Basic quota.

Optional future:

- `ADZUNA_APP_ID`
- `ADZUNA_APP_KEY`
- `GOOGLE_ALERT_FEEDS`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASS`
- `EMAIL_TO`
- `EMAIL_FROM`

Repository Actions setting:

`Settings -> Actions -> General -> Workflow permissions -> Read and write permissions`

Never commit secrets to the repository.
