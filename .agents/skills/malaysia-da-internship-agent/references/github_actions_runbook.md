# GitHub Actions Runbook

## Required repository settings

1. Repository should be private unless user intentionally wants it public.
2. `Settings -> Secrets and variables -> Actions` must contain:
   - `JSEARCH_API_KEY`
   - `JSEARCH_MAX_REQUESTS_PER_RUN`
3. `Settings -> Actions -> General -> Workflow permissions` should be set to `Read and write permissions` if the workflow commits generated CSV/DB updates.

## Required workflow structure

File: `.github/workflows/daily.yml`

Expected properties:

- `workflow_dispatch` enabled for manual runs.
- schedule twice daily.
- `permissions: contents: write`.
- Python setup with 3.11.
- install requirements.
- run `python -m src.main`.
- commit output files.

## Correct workflow example

```yaml
name: Malaysia DA Internship Finder

on:
  schedule:
    - cron: "30 0,12 * * *"
  workflow_dispatch:

permissions:
  contents: write

jobs:
  collect-rank-notify:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run internship finder
        env:
          JSEARCH_API_KEY: ${{ secrets.JSEARCH_API_KEY }}
          JSEARCH_MAX_REQUESTS_PER_RUN: ${{ secrets.JSEARCH_MAX_REQUESTS_PER_RUN }}
          ADZUNA_APP_ID: ${{ secrets.ADZUNA_APP_ID }}
          ADZUNA_APP_KEY: ${{ secrets.ADZUNA_APP_KEY }}
          GOOGLE_ALERT_FEEDS: ${{ secrets.GOOGLE_ALERT_FEEDS }}
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
          SMTP_HOST: ${{ secrets.SMTP_HOST }}
          SMTP_PORT: ${{ secrets.SMTP_PORT }}
          SMTP_USER: ${{ secrets.SMTP_USER }}
          SMTP_PASS: ${{ secrets.SMTP_PASS }}
          EMAIL_TO: ${{ secrets.EMAIL_TO }}
          EMAIL_FROM: ${{ secrets.EMAIL_FROM }}
          DB_PATH: data/jobs.db
          CSV_EXPORT_PATH: data/latest_ranked_jobs.csv
          MAX_RESULTS_PER_RUN: "80"
          MIN_SCORE_TO_NOTIFY: "55"
        run: python -m src.main

      - name: Commit database and CSV changes
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add data/jobs.db data/latest_ranked_jobs.csv data/today_shortlist.csv data/internship_tracker.csv || true
          git commit -m "Update internship job data" || echo "No changes to commit"
          git push || true
```

## Common errors

### Invalid workflow YAML line 15 or line 28

Usually caused by indentation errors around `steps:` or `env:`. Replace the entire workflow with a known-good YAML rather than editing small spaces manually.

### 403 on git push from action

Enable `Settings -> Actions -> General -> Workflow permissions -> Read and write permissions`.

### `JSEARCH_API_KEY not set`

Check GitHub Secrets names. Use exact uppercase names.

### Warning about Node.js deprecation

If status is Success, this is not urgent. Later upgrade GitHub Actions versions when official actions release newer runtimes.
