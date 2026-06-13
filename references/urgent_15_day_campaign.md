# 15-Day Urgent Internship Campaign

This mode is for the user's short, high-intensity Malaysia Data Analyst Internship search window.

## Request Budget

- OpenWeb Ninja JSearch plan: Pro, 10,000 requests/month.
- Automation target: 4 GitHub Actions runs/day.
- Per-run target: 160 JSearch requests.
- 15-day usage: 4 * 160 * 15 = 9,600 automated requests.
- Reserve: about 400 requests for manual validation and debugging.
- Workflow retention target: `MAX_RESULTS_PER_RUN=800` so useful C-level SME roles are not discarded before storage.
- Campaign guard: `config.yml` caps urgent mode at 160 requests/run until `strategy.urgent_campaign.ends_before`.
- Current rollback date: `2026-06-28`, after which JSearch falls back to `post_campaign_max_requests_per_run`.

The API key stays in `.env` and GitHub Secrets. Do not commit secrets.

## Schedule

GitHub Actions uses UTC:

- `30 4,10,15,22 * * *`

Malaysia time:

- 12:30 MYT
- 18:30 MYT
- 23:30 MYT
- 06:30 MYT next day

## Search Strategy

The query pool is grouped so each run gets a mix of:

- G1 Core Data Internship
- G2 BI / SQL / Reporting
- G3 Business / Operations Analytics
- G4 Malay / Local Internship Terms
- G5 Tier A Company Targeted
- G6 Tier B / MNC / Manufacturing
- G7 Malaysia-wide backup

`src/sources/jsearch.py` interleaves query groups before rotation. This avoids spending a run only on one category when the pool is larger than the per-run cap.

## Bucket Migration Plan

Keep the current buckets during this patch:

- `A_APPLY_NOW`
- `B_APPLY_SOON`
- `C_MASS_APPLY`
- `D_LOW_PRIORITY`

Future bucket split can be added after one or two campaign runs are reviewed:

- `A0_OFFICIAL_APPLY_NOW`
- `A1_VERIFY_THEN_APPLY`
- `B0_TIER_COMPANY_APPLY`
- `B1_SME_HIGH_PROBABILITY`
- `C0_MASS_APPLY`
- `C1_COLD_OUTREACH`
- `D_LOW_PRIORITY`

Do not rename buckets until tracker CSV consumers and notification text are updated together.
