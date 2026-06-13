# Project Memory

## User goal

The user needs a Data Analyst Internship in Malaysia for an academic requirement. The key internship period is 2026-08-02 to 2026-11-03, approximately 3 months. Internships longer than 3 months are acceptable if they can satisfy or align with this period.

## Priority locations

Final priority order:

1. Johor
2. Selangor
3. Kuala Lumpur
4. Penang
5. Malaysia-wide fallback

Johor is important for cost and practical feasibility. Selangor and Kuala Lumpur have the highest density of analytics internships. Penang matters for semiconductor, manufacturing analytics, supply chain analytics, and MNC roles.

## Role targets

Primary:

- Data Analyst Intern
- Data Analytics Intern
- BI Intern / Business Intelligence Intern
- Reporting Intern
- SQL Intern
- Power BI Intern
- Business Analyst Intern
- Data Science Intern

Malay / local terms:

- latihan industri data
- praktikal data analytics
- praktikal data analyst
- industrial training data analyst

## Company priorities

Tier 1 examples:

- Petronas
- Grab
- TNG Digital
- Shopee
- AirAsia / Capital A
- Maybank
- CIMB
- Public Bank
- RHB
- Deloitte
- PwC
- EY
- KPMG
- Accenture
- Intel
- AMD
- Bosch
- Keysight
- Micron
- Western Digital
- Maxis
- CelcomDigi
- Telekom Malaysia

Tier 2 examples:

- Abbott
- Allianz
- NTT Data
- AXA
- Mettler-Toledo
- Jabil
- Flex
- DHL
- Roche
- Siemens

SMEs remain useful for offer probability and should be placed into `C_MASS_APPLY` rather than removed.

## Current deployment history

The project was deployed from Windows CMD into a GitHub repository. GitHub Actions initially failed due to YAML indentation, then was fixed by replacing `.github/workflows/daily.yml` with valid YAML. GitHub Actions later succeeded. V2 optimization was applied and also succeeded in GitHub Actions.

## Current outputs

- `data/latest_ranked_jobs.csv`: full ranked results.
- `data/today_shortlist.csv`: shortlist organized by A/B/C buckets.
- `data/internship_tracker.csv`: application tracker.
- `data/jobs.db`: persistent dedupe/history database.

## Current API plan

OpenWeb Ninja JSearch Basic is used with around 200 requests/month. The GitHub Secret `JSEARCH_MAX_REQUESTS_PER_RUN` is set to `3`, and the workflow runs twice daily. This keeps monthly API use around 180 requests.

If the user upgrades OpenWeb Ninja JSearch, increase `JSEARCH_MAX_REQUESTS_PER_RUN` to 20-40 depending on quota. Buying ChatGPT Pro does not increase OpenWeb Ninja API quota.
