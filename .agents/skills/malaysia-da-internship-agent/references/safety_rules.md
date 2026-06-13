# Safety and Secrets Rules

## Secrets

Never expose or commit:

- `.env`
- API keys
- Telegram bot token
- Telegram chat ID if user considers it private
- SMTP password
- GitHub token
- OpenAI token

Use GitHub repository Secrets for cloud deployment.

## Required `.gitignore` entries

```text
.env
.venv/
__pycache__/
*.pyc
.pytest_cache/
data/*.db-shm
data/*.db-wal
backup_v2_*/
```

Depending on user preference, `data/jobs.db` and CSV outputs may be committed because GitHub Actions updates them. Never commit secret-bearing files.

## Logging

Logs may include job titles and apply URLs. Logs must not include secrets.

## Scraping policy

Prefer APIs and public pages. Do not implement tools that bypass access controls. Do not automate protected job platforms.

## Git workflow safety

Before every commit:

```cmd
git status
```

Confirm `.env` and `.venv` are absent from staged files.

If a secret is accidentally committed:

1. Immediately rotate the secret at the provider.
2. Remove it from the repo.
3. Treat Git history as compromised.
4. Use GitHub secret scanning/remediation workflow if available.
