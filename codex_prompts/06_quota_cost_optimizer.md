# Prompt 06 — Quota and Cost Optimizer

Use `AGENTS.md` and the `malaysia-da-internship-agent` skill.

Task:
1. Inspect JSearch request usage strategy and query rotation.
2. Assume free OpenWeb Ninja Basic quota may be 200 requests/month unless config says otherwise.
3. Keep current safe default around 3 requests/run, twice daily, unless I explicitly confirm a paid API upgrade.
4. Improve coverage under low quota by rotating query/location pairs across runs.
5. Ensure high-priority locations still receive sufficient coverage: Johor, Selangor, KL, Penang.
6. Prevent repeated identical queries from consuming the whole monthly quota.
7. Add logs that show query count and selected query pairs without printing secrets.
8. Suggest paid-quota changes separately, clearly distinguishing OpenWeb Ninja API quota from ChatGPT/Codex plan limits.
