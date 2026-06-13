# Prompt 08 — Pre-Merge Review

Before committing a major change, run a focused review.

Spawn subagents if available:
- `security_reviewer` for secrets/scraping/permissions risk.
- `scoring_evaluator` for ranking quality risk.
- `devops_release_manager` for GitHub Actions and deployment risk.

Review checklist:
1. No `.env`, `.venv`, API key, token, or password staged.
2. GitHub Actions YAML is valid.
3. Local dry-run passes.
4. API calls are quota-safe.
5. CSV outputs are still generated.
6. Tracker user fields are preserved.
7. No disallowed scraping added.
8. New dependencies are justified.
9. Changes are small enough to review.

Return blockers first, then non-blocking improvements.
