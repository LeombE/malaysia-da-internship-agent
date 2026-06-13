# Troubleshooting

## Local CMD starts in wrong folder

Symptom: `No module named src`, files not found.

Fix: Open repository folder in File Explorer, click address bar, type `cmd`, press Enter. Confirm:

```cmd
dir
```

You should see `src`, `config.yml`, `requirements.txt`.

## Python not found

Try:

```cmd
py --version
```

If still not found, install Python and add it to PATH.

## Virtual environment not active

Run:

```cmd
.venv\Scripts\activate.bat
```

## Git not found

Install Git for Windows and reopen CMD. Verify:

```cmd
git --version
```

## JSearch returns `slice(None, 10, None)` or parser errors

The API response structure may differ. Inspect response keys safely without printing secrets. Parser should accept lists and nested dicts with `data`, `jobs`, `results`, or similar keys.

## No jobs found

Check:

- API key exists locally or in GitHub Secrets.
- Request cap is not zero.
- Query rotation is not stuck on low-yield queries.
- CSV may still have old jobs; `new:0 updated:X` can be normal.

## GitHub Actions invalid YAML

Replace the entire workflow with known-good YAML from `github_actions_runbook.md`.

## GitHub Actions cannot push CSV/DB

Set repository workflow permissions to read/write.

## Quota concerns

Use:

```cmd
set JSEARCH_MAX_REQUESTS_PER_RUN=1
python -m src.main --dry-run
set JSEARCH_MAX_REQUESTS_PER_RUN=
```

Do not run repeated full tests on free API quota.
