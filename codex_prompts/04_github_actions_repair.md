# Prompt 04 — GitHub Actions Repair

Use `AGENTS.md` and the `devops_release_manager` subagent if available.

Task:
1. Inspect `.github/workflows/daily.yml`.
2. Inspect latest failure logs if available.
3. Identify whether the failure is YAML syntax, dependency install, Python runtime, missing secret, permission, or script failure.
4. If YAML syntax is invalid, replace with known-good workflow rather than manually fiddling with whitespace.
5. Preserve these requirements:
   - `workflow_dispatch` enabled.
   - scheduled twice daily for Malaysia time.
   - `permissions: contents: write`.
   - secrets through `${{ secrets.NAME }}` only.
   - run `python -m src.main`.
   - commit data outputs safely.
6. After fix, run a local YAML sanity check if possible or explain what GitHub will validate.
7. Commit and push only after `git status` confirms no `.env` or `.venv`.
