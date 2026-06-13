---
name: malaysia-da-internship-agent
description: Use this skill when maintaining, debugging, deploying, or upgrading the Malaysia Data Analyst Internship Finder project, including local Windows setup, GitHub Actions, JSearch quota, scoring algorithms, source integrations, tracker CSVs, Telegram notifications, and safe GitHub deployment.
---

# Malaysia Data Analyst Internship Agent Skill

## Scope

This skill is for a specific project: a Python + GitHub Actions agent that finds Malaysia Data Analyst Internship opportunities, ranks them, writes CSV/SQLite outputs, and runs automatically twice daily.

Use this skill when the user asks for:

- local setup or deployment from zero,
- Git/GitHub upload steps,
- GitHub Actions workflow fixes,
- API key / GitHub Secrets setup guidance,
- JSearch quota strategy,
- scoring or filtering improvements,
- source integration,
- Telegram/email notifications,
- internship tracker improvements,
- daily maintenance prompts,
- project transfer to Codex.

## Project objective

Maximize the user's chance of securing a Malaysia-based Data Analyst Internship aligned with 2026-08-02 to 2026-11-03. The system should focus on Johor, Selangor, Kuala Lumpur, and Penang, while keeping Malaysia-wide fallback roles.

## Required first steps before changing code

1. Read `AGENTS.md`.
2. Read `README_V2_OPTIMIZATIONS.md` if present.
3. Inspect `config.yml`, `src/scoring.py`, `src/sources/jsearch.py`, `src/storage.py`, `src/main.py`, `.github/workflows/daily.yml`.
4. Inspect `data/today_shortlist.csv` and `data/latest_ranked_jobs.csv` if present.
5. Summarize current status and propose a minimal plan.

## Safe local validation

Use this command for a quota-safe local test:

```cmd
set JSEARCH_MAX_REQUESTS_PER_RUN=1
python -m src.main --dry-run
set JSEARCH_MAX_REQUESTS_PER_RUN=
```

Use this command for full local dry-run based on `.env`:

```cmd
python -m src.main --dry-run
```

Do not run repeated API tests unless necessary. The user may be on the OpenWeb Ninja Basic plan with 200 requests/month.

## GitHub Actions validation

The workflow should:

- run on `ubuntu-latest`,
- install Python 3.11,
- install `requirements.txt`,
- read secrets through GitHub Secrets,
- run `python -m src.main`,
- commit `data/jobs.db`, `data/latest_ranked_jobs.csv`, `data/today_shortlist.csv`, and `data/internship_tracker.csv` where appropriate.

## Security rules

- Never ask the user to paste secrets into chat or logs.
- Never include `.env` in commits.
- Never add automated scraping that violates login/CAPTCHA/robots/terms restrictions.
- Prefer APIs, official ATS pages, public RSS/Atom, Google Alerts RSS, and company career pages.
- If a source is legally or technically questionable, propose a safer alternative.

## Scoring improvement rules

When improving scoring, preserve this strategic balance:

- Big companies get bonus, but SMEs stay in the mass-apply pool.
- Official career page / ATS link gets bonus.
- Aggregators get a modest penalty, not deletion.
- Johor/Selangor/KL/Penang are location priorities.
- Hireability and role fit matter more than salary.
- Date fit for Aug-Nov 2026 matters, but missing date should not automatically delete a role because many internship posts do not state future intake windows.

## Output quality requirements

Every output row should ideally include:

- job_id,
- source,
- title,
- company,
- location,
- state,
- score,
- bucket,
- recommended_action,
- apply_url,
- reasons,
- first_seen,
- last_seen.

## References to read when needed

- `references/project_memory.md`
- `references/deployment_runbook_windows.md`
- `references/github_actions_runbook.md`
- `references/scoring_strategy.md`
- `references/source_integration_policy.md`
- `references/safety_rules.md`
- `references/troubleshooting.md`
