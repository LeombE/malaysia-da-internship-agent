You are working in my GitHub repo `malaysia-da-internship-agent`.

Mission: turn today's collected Malaysia data analyst internship results into a better application plan and improve tomorrow's search quality.

Evening task:
1. Read `data/latest_ranked_jobs.csv` and `data/jobs.db`.
2. Group results into A/B/C/D priority:
   - A: official company page or reliable source, strong data/analytics internship match, location matches Johor/Selangor/KL/Penang, likely fits 2026-08-02 to 2026-11-03 or minimum 3 months.
   - B: strong role match but date or source is unclear.
   - C: smaller companies with high acceptance probability.
   - D: full-time/senior/manager/not internship/poor location/low relevance.
3. Improve scoring in `src/scoring.py` only if the current ranking is clearly wrong.
4. Add missing high-value companies or career URLs to `data/company_targets.yml` only when the URL is public and suitable for a personal job-search monitor.
5. Produce tomorrow's application shortlist: top 10 apply-now jobs, top 10 monitor jobs, and exact reasons.
6. Do not bypass login, CAPTCHA, robots.txt, or any platform restriction.
7. Run `python -m src.main --dry-run` and summarize whether the code still works.

Make minimal, reviewable commits/PR changes.
