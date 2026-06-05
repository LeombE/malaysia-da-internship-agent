# V2 Optimizations

This repo has been upgraded for a realistic Malaysia Data Analyst Internship search strategy.

## What changed

- Location priority now follows the user's actual preference: Johor, Selangor, Kuala Lumpur, Penang, Malaysia.
- JSearch queries rotate each GitHub Actions run so a 3-request Basic API cap can still cover different query-location pairs over time.
- Scoring now balances realistic offer probability, not just brand prestige.
- Official career pages / ATS links are boosted.
- Low-signal aggregators such as trabajo/jobleads/jooble are penalized but not deleted, because mass-apply strategy still needs coverage.
- Duplicate postings are reduced by canonical title + company + location matching.
- New CSV outputs:
  - `data/latest_ranked_jobs.csv`: all ranked jobs.
  - `data/today_shortlist.csv`: actionable A/B/C shortlist.
  - `data/internship_tracker.csv`: application tracker where statuses can be manually updated.

## Buckets

- `A_APPLY_NOW`: apply today after checking date/duration.
- `B_APPLY_SOON`: apply within 48 hours.
- `C_MASS_APPLY`: useful for high-volume applications.
- `D_LOW_PRIORITY`: low fit/noisy; ignore unless manually relevant.

## API quota

With `JSEARCH_MAX_REQUESTS_PER_RUN=3` and 2 scheduled runs/day, expected usage is about 180 requests/month, which fits the Basic 200-request/month plan.
