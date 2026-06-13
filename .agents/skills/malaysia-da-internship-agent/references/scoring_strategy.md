# Scoring Strategy

## Goal

Rank jobs by practical internship value, not by prestige alone. The user needs an internship offer that can satisfy an academic requirement around 2026-08-02 to 2026-11-03.

## Suggested weight model

- 35% internship fit and hireability.
- 25% location fit.
- 15% company quality.
- 10% analytics skill match.
- 10% duration/date fit.
- 5% salary or benefits.

## Location priority

1. Johor
2. Selangor
3. Kuala Lumpur
4. Penang
5. Malaysia

## Positive signals

- intern, internship, practical training, industrial training, trainee.
- student, undergraduate, final year, degree, diploma.
- 3 months, minimum 3 months, Aug 2026, Summer 2026 if it may cover the academic window, intake.
- data analyst, analytics, BI, reporting, dashboard, SQL, Power BI, Python, Excel, Tableau, data science, business analyst.
- official company career page or ATS apply URL.
- reputable employer or clear department.

## Negative signals

- senior, manager, director, lead.
- permanent, full-time non-internship.
- 2+ or 3+ years required.
- country mismatch such as South Africa, India, United States, Singapore-only, if not remote Malaysia.
- undisclosed company.
- aggregator source with no clear original apply path.

## Source scoring

Use modest source adjustments:

- Official career page: +20.
- ATS such as Workday, Greenhouse, Lever, SmartRecruiters, SuccessFactors: +15.
- Mainstream job board: +5.
- Aggregator such as Jooble, Trabajo, JobLeads: -10.

Do not delete aggregator jobs. Some SMEs only appear through aggregator pipelines. Keep them in `C_MASS_APPLY` unless other signals make them poor.

## Buckets

`A_APPLY_NOW`: strong role fit, credible company/source, good location, likely internship.

`B_APPLY_SOON`: good role, needs quick manual verification of source/date/duration.

`C_MASS_APPLY`: lower certainty, SMEs, aggregators, or generic internship posts that are still useful for high-volume applications.

`D_LOW_PRIORITY`: noise, wrong geography, senior/full-time, weak role fit, or low confidence.
