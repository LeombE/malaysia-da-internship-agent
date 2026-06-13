# Codex Transfer Summary for Human

This repository is a Malaysia Data Analyst Internship Finder for a student internship requirement.

Important facts:

- Internship window: 2026-08-02 to 2026-11-03.
- Target duration: about 3 months; longer is acceptable if it covers the window.
- Locations: Johor, Selangor, Kuala Lumpur, Penang, Malaysia fallback.
- Priority: offer probability and practical fit over salary.
- Company strategy: prioritize large/high-quality companies but keep SMEs for mass applications.
- Main source: OpenWeb Ninja JSearch API.
- Current quota strategy: 3 requests/run, twice daily, around 180/month.
- GitHub Actions is working.
- V2 scoring and tracker are deployed.
- Output files are in `data/`.

Codex should improve the project safely by:

1. Checking logs and CSV quality.
2. Improving scoring and dedupe.
3. Adding Telegram notifications.
4. Adding safe sources.
5. Maintaining quota discipline.
6. Never committing secrets.
7. Avoiding disallowed scraping.

First Codex prompt to use: `codex_prompts/00_master_bootstrap.md`.
