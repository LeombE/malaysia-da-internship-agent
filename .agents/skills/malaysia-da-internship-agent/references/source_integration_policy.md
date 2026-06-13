# Source Integration Policy

## Preferred source types

1. Official company career pages.
2. Official ATS endpoints/pages: Workday, Greenhouse, Lever, SmartRecruiters, SuccessFactors, Teamtailor, Ashby where public.
3. Jobs APIs such as JSearch and Adzuna.
4. Google Alerts RSS feeds.
5. Public RSS/Atom feeds.
6. Public web pages only when allowed and technically simple.

## Disallowed or high-risk patterns

Do not implement:

- login-based scraping,
- CAPTCHA bypass,
- proxy rotation to evade rate limits,
- scraping platforms that disallow automated scraping in terms/robots,
- browser automation against LinkedIn/Jobstreet login sessions,
- storing credentials in repo.

## Aggregator handling

Aggregator links are allowed but lower confidence. Prefer official apply links if discoverable from job metadata or description. If only aggregator exists, keep it as mass-apply candidate.

## New source acceptance checklist

Before adding a source, verify:

- Source is legal and low-risk.
- It does not require login/captcha bypass.
- It has stable fields or a robust parser.
- It has rate limiting / timeout handling.
- It can be disabled via config or missing key.
- It produces normalized job objects.
- It does not expose secrets in logs.
- It is covered by dry-run validation.

## Integration target output

Every source should normalize into the same internal schema with:

- source
- source_url
- apply_url
- title
- company
- location
- state
- description
- posted_at if available
- raw metadata if useful
