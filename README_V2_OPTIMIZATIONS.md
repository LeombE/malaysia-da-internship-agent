# Optimization History

This file summarizes the major improvements after the original starter project.

## V2: Practical Internship Ranking

The first optimization pass changed the project from a simple job collector into a more realistic internship decision pipeline.

Key improvements:

- Location priority now follows the user's actual preference: Johor, Selangor, Kuala Lumpur, Penang, then Malaysia-wide fallback.
- Scoring balances practical offer probability, not only brand prestige.
- Official career pages and ATS links receive source-quality bonuses.
- Low-signal aggregators receive penalties but are not deleted because SME and mass-apply coverage still matters.
- Duplicate postings are reduced by canonical title, company, and location matching.
- CSV outputs were expanded:
  - `data/latest_ranked_jobs.csv`: full ranked output.
  - `data/today_shortlist.csv`: actionable A/B/C shortlist.
  - `data/internship_tracker.csv`: application tracker with user-editable status fields.

## V3: Source-Quality Calibration

The source-quality pass reduced the impact of weak aggregator-only links while preserving broad discovery.

Key improvements:

- Added observed low-signal domains such as Expertini, BeBee, Prosple, WhatJobs, Maukerja, and Built In to the source-quality calibration.
- Increased the aggregator/secondary-source penalty without blocking those roles.
- Kept official company career pages and ATS links preferred.
- Preserved SME and mass-apply opportunities in `C_MASS_APPLY`.

## V3: 15-Day Urgent Internship Campaign

The urgent campaign uses the OpenWeb Ninja Pro plan for high-coverage internship discovery during a short search window.

Campaign strategy:

- GitHub Actions runs 4 times per day.
- `JSEARCH_MAX_REQUESTS_PER_RUN=160` during the campaign.
- Approximate 15-day automated budget: `4 * 160 * 15 = 9,600` requests.
- About 400 requests remain for manual validation/debug from the 10,000/month Pro plan.
- The query pool is expanded across:
  - G1 Core Data Internship
  - G2 BI / SQL / Reporting
  - G3 Business / Operations Analytics
  - G4 Malay / Local Internship Terms
  - G5 Tier A Company Targeted
  - G6 Tier B / MNC / Manufacturing
  - G7 Malaysia-wide backup

The urgent campaign runs four times per day in Malaysia time:

- 06:30 MYT
- 12:30 MYT
- 18:30 MYT
- 23:30 MYT

GitHub Actions implements that schedule with this UTC cron:

```yaml
cron: "30 4,10,15,22 * * *"
```

## Current Output Snapshot

Latest checked output snapshot as of `2026-06-14T23:59:52+00:00`.

These metrics are generated outputs and will change after scheduled GitHub Actions runs.

| Output | Rows |
|---|---:|
| `data/latest_ranked_jobs.csv` | 500 |
| `data/today_shortlist.csv` | 80 |
| `data/internship_tracker.csv` | 353 |
| Newest campaign rows in `latest_ranked_jobs.csv` | 420 |

Newest campaign bucket counts:

| Bucket | Rows |
|---|---:|
| `A_APPLY_NOW` | 10 |
| `B_APPLY_SOON` | 61 |
| `C_MASS_APPLY` | 226 |
| `D_LOW_PRIORITY` | 123 |

Newest campaign location coverage:

| State | Rows |
|---|---:|
| Selangor | 154 |
| Kuala Lumpur | 132 |
| Penang | 82 |
| Johor | 21 |
| Malaysia-wide | 30 |
| Unclassified | 1 |

## Portfolio Value

These optimizations demonstrate:

- API-driven data collection.
- Configurable query strategy.
- Automated scheduling with GitHub Actions.
- Data cleaning and deduplication.
- Business-rule scoring.
- Decision-ready reporting.
- Responsible quota and secrets management.

See `docs/portfolio_case_study.md`, `docs/data_dictionary.md`, `docs/scoring_methodology.md`, and `reports/latest_campaign_summary.md` for recruiter and stakeholder-facing documentation.
