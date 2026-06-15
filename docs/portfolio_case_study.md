# Portfolio Case Study: Malaysia Data Analyst Internship Intelligence Pipeline

## Problem

The user needs a Malaysia-based Data Analyst, Data Analytics, BI, Business Analyst, Reporting, SQL, Power BI, or Data Science internship around 2026-08-02 to 2026-11-03.

The search problem is noisy:

- Job listings are duplicated across official sites, job boards, and aggregators.
- Many postings do not state the exact internship intake period.
- Aggregator listings can be stale or rewritten.
- The user needs to act quickly but still preserve SME and mass-apply opportunities.
- The highest-value decision is not salary maximization; it is increasing the probability of receiving a suitable internship offer.

## Stakeholders

Primary stakeholder:

- The internship applicant who needs a decision-ready shortlist and application tracker.

Secondary stakeholders:

- Academic internship coordinator, who needs evidence of a structured search process.
- Recruiters or hiring managers, who can review this repository as proof of applied data pipeline skills.
- Future maintainers, who need a safe automation and quota strategy.

## Decision Improved

The pipeline improves this decision:

> Which internship opportunities should be applied to today, verified first, mass-applied to, or ignored?

It turns raw job search results into ranked action buckets:

- `A_APPLY_NOW`: apply today after checking date/duration.
- `B_APPLY_SOON`: apply within 48 hours after quick verification.
- `C_MASS_APPLY`: keep for high-volume applications and SME coverage.
- `D_LOW_PRIORITY`: keep for audit/history but usually ignore.

## Pipeline Built

The project implements a repeatable data workflow:

1. Collect job records from OpenWeb Ninja JSearch API and optional safe sources.
2. Normalize titles, companies, locations, URLs, timestamps, descriptions, and source metadata.
3. Score jobs using role fit, location fit, internship/date fit, company tier, source quality, and risk penalties.
4. Store records in SQLite with first-seen and last-seen timestamps.
5. Deduplicate ranked outputs while preferring official/ATS links over low-confidence aggregators.
6. Export decision-ready CSVs:
   - `data/latest_ranked_jobs.csv`
   - `data/today_shortlist.csv`
   - `data/internship_tracker.csv`
7. Run automatically through GitHub Actions.

## Current Campaign Metrics

Latest checked output snapshot as of `2026-06-14T23:59:52+00:00`.

These metrics are generated outputs and will change after scheduled GitHub Actions runs.

| Metric | Value |
|---|---:|
| `latest_ranked_jobs.csv` rows | 500 |
| `today_shortlist.csv` rows | 80 |
| `internship_tracker.csv` rows | 353 |
| Newest campaign rows in `latest_ranked_jobs.csv` | 420 |
| Newest `A_APPLY_NOW` rows | 10 |
| Newest `B_APPLY_SOON` rows | 61 |
| Newest `C_MASS_APPLY` rows | 226 |
| Newest `D_LOW_PRIORITY` rows | 123 |
| Newest Selangor rows | 154 |
| Newest Kuala Lumpur rows | 132 |
| Newest Penang rows | 82 |
| Newest Johor rows | 21 |
| Newest Malaysia-wide rows | 30 |
| Newest unclassified rows | 1 |

Automation:

- 4 GitHub Actions runs per day.
- 160 JSearch requests per run during the urgent campaign.
- Approximate 15-day request target: 9,600 automated requests.
- Approximate reserve: 400 requests for validation/debug.

## Business Impact

The project reduces manual search time and improves application priority by:

- Converting noisy search results into a ranked shortlist.
- Highlighting official and ATS links when available.
- Preserving lower-confidence SME roles for mass application rather than deleting them.
- Tracking which opportunities were first seen and last seen.
- Creating a reusable application tracker with status and follow-up fields.
- Giving the applicant a daily operating rhythm for applying, verifying, and following up.

## Data Limitations

Known limitations:

- Many internship postings do not state exact Aug-Nov 2026 intake compatibility.
- Aggregator-heavy results can include stale, duplicated, or rewritten job descriptions.
- Some official application links may need manual search if JSearch returns an aggregator page.
- Location extraction can be imperfect when listings mention multiple cities or when URLs contain city text.
- `internship_tracker.csv` requires manual updates for applied status, follow-up dates, interviews, and offers.
- The score ranks practical fit; it does not guarantee that a role remains open.

## Why This Is Relevant for a Data Analyst Internship

This project demonstrates applied Data Analyst skills in a realistic stakeholder setting:

- It defines a business problem and turns it into measurable decision rules.
- It collects data from APIs and public sources.
- It cleans and standardizes semi-structured job data.
- It creates scoring logic that balances competing stakeholder needs.
- It builds automated reports and application tracking outputs.
- It explains limitations, confidence, and recommended actions.
- It uses GitHub Actions, SQLite, Python, and CSV reporting in a production-like workflow.

## Resume Bullets

- Built an automated Python job-intelligence pipeline that collects, scores, ranks, and exports Malaysia internship leads for stakeholder decision-making.
- Designed scoring logic across role relevance, location priority, internship/date fit, company tier, source quality, and risk penalties.
- Automated a 15-day urgent search campaign through GitHub Actions with 4 daily runs and 160 JSearch requests per run.
- Produced ranked CSV outputs and a tracker that support daily apply, verify, mass-apply, and follow-up workflows.
- Applied responsible sourcing and secret-management practices by using APIs, public sources, GitHub Secrets, and no login scraping.
