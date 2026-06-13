# Windows Local Deployment Runbook

## Starting point

Repository root should contain:

- `.github`
- `data`
- `prompts` or `codex_prompts`
- `src`
- `config.yml`
- `requirements.txt`
- `.env.example`

## Open CMD in correct folder

In Windows File Explorer, open the repository folder. Click the address bar, type:

```text
cmd
```

Press Enter.

## Create and activate virtual environment

```cmd
python --version
python -m venv .venv
.venv\Scripts\activate.bat
```

If `python` is not recognized, try `py` or install Python and add it to PATH.

## Install dependencies

```cmd
pip install -r requirements.txt
```

## Create `.env`

Only once:

```cmd
copy .env.example .env
```

Never repeat this after adding real secrets, because it can overwrite local `.env`.

## Add local API key

Open:

```cmd
notepad .env
```

Add:

```text
JSEARCH_API_KEY=<your_openweb_ninja_key>
JSEARCH_MAX_REQUESTS_PER_RUN=3
```

No quotes, no spaces, and never share this value.

## Dry-run test

```cmd
python -m src.main --dry-run
```

Quota-safe test:

```cmd
set JSEARCH_MAX_REQUESTS_PER_RUN=1
python -m src.main --dry-run
set JSEARCH_MAX_REQUESTS_PER_RUN=
```

## Open outputs

```cmd
start data\latest_ranked_jobs.csv
start data\today_shortlist.csv
start data\internship_tracker.csv
```

## Git safety

Before commit:

```cmd
git status
```

Confirm `.env` and `.venv` are not staged.
