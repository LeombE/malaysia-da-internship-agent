# Prompt 05 — New Source Integration

Use `AGENTS.md`, the `malaysia-da-internship-agent` skill, and the `source_integrator` subagent if available.

Task:
1. Propose one safe new source integration that improves coverage for Malaysia data internships.
2. Preferred order:
   - Adzuna API if keys are available.
   - Google Alerts RSS feeds.
   - Public company career pages / ATS pages.
3. Do not implement login scraping, CAPTCHA bypass, protected platform scraping, or robots/terms-violating extraction.
4. Normalize source results to the existing job schema.
5. Make source failures graceful when keys/feeds are missing.
6. Add source-specific timeout and error handling.
7. Update scoring to account for source quality without over-penalizing SMEs.
8. Run dry-run validation with low API quota.
9. Document required GitHub Secrets or config changes.
