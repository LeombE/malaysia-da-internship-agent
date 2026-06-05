You are working in my GitHub repo `malaysia-da-internship-agent`.

Mission: improve the reliability and coverage of my Malaysia data analyst internship agent for the target internship period 2026-08-02 to 2026-11-03, with priority locations Johor, Selangor, Kuala Lumpur, and Penang. Big companies should be prioritized before smaller companies, but the practical goal is getting an internship offer.

Morning task:
1. Inspect the latest workflow run logs, `data/latest_ranked_jobs.csv`, `data/jobs.db`, and source code.
2. Identify failed or low-yield sources, duplicate issues, weak query coverage, or scoring mistakes.
3. Add or improve queries for data analyst intern, data analytics intern, BI intern, business analyst intern, Power BI intern, SQL intern, data science intern, latihan industri data, and praktikal data.
4. Improve `config.yml` and `data/company_targets.yml` if coverage is weak, especially Tier-1 companies in Malaysia with KL/Selangor/Penang/Johor presence.
5. Do not add scraping that bypasses login, CAPTCHA, robots.txt, or platform terms. Prefer official APIs, RSS/Atom, Google Alerts, and public company career pages.
6. Run tests or at least `python -m src.main --dry-run` with mocked/missing keys handled gracefully.
7. Return a concise changelog, risks, and next recommended manual actions.

Make minimal, reviewable commits/PR changes.
