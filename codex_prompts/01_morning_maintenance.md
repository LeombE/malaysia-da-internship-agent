# Prompt 01 — Morning Maintenance

Use `AGENTS.md` and the `malaysia-da-internship-agent` skill.

Morning maintenance task:
1. Inspect the latest GitHub Actions workflow status if available.
2. Inspect `data/latest_ranked_jobs.csv`, `data/today_shortlist.csv`, `data/internship_tracker.csv`, and recent code changes.
3. Check if the output quality aligns with my internship goals: Johor, Selangor, KL, Penang; 2026-08-02 to 2026-11-03; Data Analyst/Data Analytics/BI/SQL/Power BI; offer probability over salary.
4. Identify bad rows: non-Malaysia roles, senior/full-time/permanent roles, South Africa/India/USA/Singapore-only mismatches, low-confidence aggregators, duplicates, wrong titles.
5. Recommend minimal scoring/query/source improvements.
6. If code changes are needed, make small patches only.
7. Run a quota-safe test: `set JSEARCH_MAX_REQUESTS_PER_RUN=1 && python -m src.main --dry-run` on Windows, or the equivalent shell syntax if not on Windows.
8. Show a changelog, validation result, and next manual action.
9. Confirm that `.env` and `.venv` are not staged before commit.

Do not use repeated API calls unless necessary.
