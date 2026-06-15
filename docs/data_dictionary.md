# Data Dictionary

This document explains the main output fields in the Malaysia Data Analyst Internship Intelligence Pipeline.

## Output Files

| File | Description |
|---|---|
| `data/latest_ranked_jobs.csv` | Full ranked output for auditing and deeper review. |
| `data/today_shortlist.csv` | Compact action shortlist for daily application decisions. |
| `data/internship_tracker.csv` | Application tracker with user-editable fields for status and follow-up. |

## Common Fields

| Field | Appears in | Meaning | How to interpret |
|---|---|---|---|
| `job_id` | All CSVs | Stable hash ID generated from job title, company, and location/state. | Use this as the row identifier when updating tracker status. |
| `source` | All CSVs | Source integration that found the job, such as `jsearch`. | Tells where the pipeline collected the record. |
| `title` | All CSVs | Job title. | Check if it clearly mentions intern, internship, data, analytics, BI, SQL, reporting, Power BI, or business analyst terms. |
| `company` | All CSVs | Employer or publisher company name. | Use with `title` and `apply_url` to verify whether the listing is real and current. |
| `location` | All CSVs | Raw location text from the source. | Review manually when location is broad, missing, or conflicts with `state`. |
| `state` | All CSVs | Normalized Malaysia location priority group. | Expected values include Johor, Selangor, Kuala Lumpur, Penang, and Malaysia. |
| `score` | All CSVs | Final 0-100 ranking score. | Higher scores should receive earlier action, but manual verification is still required. |
| `bucket` | All CSVs | Action category derived from score. | Use this as the daily application priority. |
| `recommended_action` | All CSVs | Plain-English action tied to the bucket. | Follow this to decide apply now, verify, mass apply, or ignore. |
| `apply_url` | All CSVs | Best known application URL. | Prefer official company or ATS links over aggregator links. |
| `source_url` | All CSVs | Source URL or backup URL. | Use when `apply_url` is missing, weak, or aggregator-only. |
| `posted_at` | `latest_ranked_jobs.csv`, `today_shortlist.csv` | Posting timestamp when available. | Missing or old dates lower confidence but do not automatically disqualify a role. |
| `first_seen_at` | All CSVs | First time the pipeline stored the job. | Helps identify newly discovered opportunities. |
| `last_seen_at` | All CSVs | Most recent run where the job appeared or was rescored. | Recent rows are better candidates for immediate review. |
| `reasons` | All CSVs | Semicolon-separated scoring explanation. | Explains why the row ranked high or low. |

## `latest_ranked_jobs.csv`

This is the broadest output and is best for audit, QA, and trend analysis.

Additional fields:

| Field | Meaning | How to interpret |
|---|---|---|
| `description` | Job description or snippet from the source. | Use to verify role fit, skills, date fit, and false positives. |
| `salary` | Salary text if available. | Salary is low priority for this project. Missing salary is not a problem. |
| `notify_count` | Number of times the job has been included in notifications. | Helps prevent repeated notifications for the same role. |
| `source_rank` | Source quality rank added during export. | `3` is official/ATS-like, `2` is trusted job board, `1` is neutral/secondary, `0` is low-signal aggregator. |

Stakeholder use:

- Audit all ranked results.
- Identify false positives.
- Review source quality.
- Compare coverage by state, bucket, and company.

## `today_shortlist.csv`

This is the daily operating file.

It includes the most important action fields and omits long descriptions so the user can scan quickly.

Stakeholder use:

1. Apply to realistic `A_APPLY_NOW` roles first.
2. Verify and apply to strong `B_APPLY_SOON` roles.
3. Use `C_MASS_APPLY` for broad application volume.
4. Copy applied roles into the tracker workflow.

## `internship_tracker.csv`

This file preserves user-editable application workflow fields while refreshing job metadata.

Tracker-specific fields:

| Field | Meaning | How to interpret |
|---|---|---|
| `applied` | Manual flag, usually yes/no. | Mark when an application has been submitted. |
| `application_date` | Date the user applied. | Use `YYYY-MM-DD` for clean tracking. |
| `status` | Current application status. | Example values: Applied, Need Follow-Up, Interview, Rejected, Offer, Withdrawn. |
| `follow_up_date` | Planned follow-up date. | Helps manage applications older than 7-10 days. |
| `interview_date` | Scheduled or completed interview date. | Use for funnel tracking. |
| `offer_status` | Offer result or negotiation status. | Useful for measuring final internship outcomes. |
| `notes` | Free-text notes. | Record verification notes, HR contact, intake date, or custom concerns. |

Current limitation:

- The tracker currently has blank status fields until the user updates application progress manually.

## Score Interpretation

| Score range | Bucket | Meaning |
|---:|---|---|
| 70-100 | `A_APPLY_NOW` | Highest practical fit. Apply today after checking date and duration. |
| 55-69 | `B_APPLY_SOON` | Strong candidate. Verify source/date and apply within 48 hours. |
| 42-54 | `C_MASS_APPLY` | Useful for volume, SME coverage, or lower-confidence leads. |
| 0-41 | `D_LOW_PRIORITY` | Weak, noisy, stale, or not clearly aligned. |

## Source Quality Interpretation

| Source quality | Typical evidence | Confidence |
|---|---|---|
| Official/ATS | Company career site, Workday, SuccessFactors, Greenhouse, Lever, SmartRecruiters | High |
| Trusted board | LinkedIn, Hiredly, Indeed, Foundit, JobStreet-style board | Medium |
| Neutral/secondary | Unknown host or secondary posting | Medium-low |
| Aggregator/low-signal | Trabajo, Jooble, Expertini, BeBee, JobLeads, similar sources | Low; verify manually |

## Reason Codes

The `reasons` field combines evidence from scoring:

- `bucket: ...`: final action category.
- `internship/practical training role`: internship language was found.
- `core role keyword`: strong data/analytics internship phrase was found.
- `adjacent analytics role keyword`: related analytics/business/data phrase was found.
- `analytics skill match`: skills such as Excel, SQL, Power BI, Python, Tableau, dashboarding, or reporting were found.
- `location priority`: matched Johor, Selangor, Kuala Lumpur, Penang, or Malaysia.
- `priority city`: matched a configured priority city.
- `duration likely fits`: internship duration appears compatible.
- `date not stated`: kept for manual confirmation instead of deleting.
- `Tier-1 target company` or `Tier-2 established company`: recognized employer bonus.
- `aggregator/low-signal source`: manual source verification needed.
- `seniority/permanent/experience red flag`: likely wrong level or non-internship risk.
- `possible non-Malaysia noise`: location/source text needs manual review.
