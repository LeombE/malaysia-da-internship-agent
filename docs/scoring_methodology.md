# Scoring Methodology

The scoring system ranks internship opportunities by practical actionability for a Malaysia Data Analyst Internship search. The goal is to increase the chance of receiving a suitable internship offer, not to maximize salary.

## Scoring Overview

Each `JobPosting` is scored from 0 to 100 using business rules in `src/scoring.py`.

Main scoring components:

1. Role relevance.
2. Location priority.
3. Internship/date/duration fit.
4. Company tier.
5. Source quality.
6. Student/resume fit.
7. Posting freshness.
8. Risk penalties.

The final score maps to an action bucket:

| Score range | Bucket | Action |
|---:|---|---|
| 70-100 | `A_APPLY_NOW` | Apply today after checking date/duration. |
| 55-69 | `B_APPLY_SOON` | Apply within 48 hours after quick verification. |
| 42-54 | `C_MASS_APPLY` | Mass-apply if role/location is acceptable. |
| 0-41 | `D_LOW_PRIORITY` | Ignore unless manually relevant. |

## 1. Role Relevance

The score rewards roles that clearly match the target internship category.

High-value role signals include:

- Data Analyst Intern
- Data Analytics Intern
- Business Intelligence Intern
- BI Intern
- Power BI Intern
- SQL Intern
- Reporting Intern
- Dashboard Intern
- Data Visualization Intern
- Data Science Intern
- Business Analyst Intern
- Operations, supply chain, finance, risk, marketing, commercial, or customer analytics intern
- Malay/local terms such as latihan industri, praktikal, and pelatih

The model also rewards technical skill matches:

- Excel
- SQL
- Power BI
- Tableau
- Python
- Dashboarding
- Reporting
- Analytics
- Data visualization
- Business intelligence
- ETL
- Databases
- Statistics

Rows that do not clearly mention internship language or data/analytics work are penalized.

## 2. Location Priority

Location scoring follows the internship search strategy:

1. Johor
2. Selangor
3. Kuala Lumpur
4. Penang
5. Malaysia-wide fallback

Preferred cities receive additional weight, including Johor Bahru, Iskandar Puteri, Skudai, Senai, Kulai, Pasir Gudang, Petaling Jaya, Subang Jaya, Shah Alam, Cyberjaya, Bangsar South, KL Sentral, George Town, Bayan Lepas, Batu Kawan, Perai, and Butterworth.

Known limitation:

- Location normalization can be imperfect when source text includes multiple cities, URLs, or broad federal territory labels. Manual review is still needed for high-priority roles.

## 3. Internship and Date Fit

The target internship window is approximately 2026-08-02 to 2026-11-03.

The model rewards:

- Internship/practical training/industrial training language.
- 3-month or 3-6-month durations.
- Aug-Nov 2026 references.
- Longer internships when they can plausibly cover the required window.

The model does not delete roles with missing dates because many Malaysian internship postings do not state future intake windows. Instead, date-missing roles are kept for manual verification.

Known limitation:

- Wrong-intake roles such as Jan-Apr 2026 or Summer 2026 may still appear and must be verified manually.

## 4. Company Tier

Company scoring reflects both reputation and offer strategy.

Tier 1 examples:

- PETRONAS
- Grab
- Shopee
- Intel
- AMD
- Bosch
- Deloitte
- PwC
- EY
- KPMG
- Accenture
- Maybank
- CIMB
- AirAsia
- Maxis
- CelcomDigi

Tier 2 examples:

- Abbott
- NTT DATA
- Allianz
- AXA
- Mettler-Toledo
- DHL
- Siemens
- Western Digital
- Micron
- Keysight
- Infineon
- Jabil
- Flex
- Roche

Unknown or SME companies are not removed. They receive lower company-tier scores but remain available for mass application because offer probability matters.

## 5. Source Quality

Source quality changes the confidence level of a row.

High-confidence sources:

- Official company career pages.
- ATS platforms such as Workday, SuccessFactors, Greenhouse, Lever, and SmartRecruiters.
- Recognized company domains such as Grab Careers, TNG Digital, Intel, PETRONAS, Bosch, Maxis, AirAsia, and similar official sites.

Medium-confidence sources:

- Trusted job boards such as LinkedIn, Hiredly, Indeed, Glassdoor, Foundit, and JobStreet-style boards.

Low-confidence sources:

- Aggregators and secondary sources such as Trabajo, Jooble, Expertini, BeBee, Prosple, WhatJobs, Maukerja, JobLeads, Talent, Jora, GrabJobs, Built In, Adzuna, and similar sources.

## 6. Official/ATS Preference

Official or ATS links receive a source-quality bonus because they are more likely to be current and actionable.

When duplicate rows are exported, the export layer prefers higher source quality before score. This helps official or trusted links win over aggregator copies when the same role appears more than once.

## 7. Aggregator Penalty

Aggregator links are penalized, not blocked.

Reason:

- Aggregators can surface useful SME opportunities.
- The user is using a mass-application strategy.
- Deleting all secondary-source roles would reduce offer probability.

The intended behavior is:

- Strong aggregator-only roles may remain in `B_APPLY_SOON`.
- Weaker aggregator-only roles should move into `C_MASS_APPLY`.
- Low-confidence noisy roles should fall into `D_LOW_PRIORITY`.

## 8. SME and Mass-Apply Preservation

The system deliberately keeps SME roles when they have reasonable data/analytics and internship signals.

Why:

- Large companies are attractive but competitive.
- SMEs may respond faster and offer more realistic conversion chances.
- The internship requirement prioritizes securing a suitable offer.

This is why `C_MASS_APPLY` exists as a productive bucket rather than a failure bucket.

## 9. Risk Penalties

The scoring system penalizes:

- Senior roles.
- Manager, lead, director, or head-of roles.
- Permanent or full-time-only language.
- 3+ years of required experience.
- Non-Malaysia location signals.
- Undisclosed/confidential companies.
- Sales-heavy or weak data-fit roles.
- Masters-level requirements when they may not match the applicant.

## 10. Known Limitations

- The model is rule-based, not a trained machine-learning classifier.
- It depends on source text quality.
- Some aggregators rewrite titles and descriptions in ways that inflate role relevance.
- Some official links may be hidden behind aggregator pages and require manual search.
- Some postings lack exact date windows.
- Some location classification errors are possible.
- The final decision still requires human review before applying.

## Practical Interpretation

Use the score and bucket as a first-pass decision aid:

1. Apply to official or trusted `A_APPLY_NOW` roles first.
2. Verify source/date on strong `B_APPLY_SOON` roles.
3. Use `C_MASS_APPLY` to maintain application volume.
4. Ignore most `D_LOW_PRIORITY` rows unless a manual review finds a special reason.
