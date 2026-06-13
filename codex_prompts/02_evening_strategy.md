# Prompt 02 — Evening Application Strategy

Use `AGENTS.md` and the `malaysia-da-internship-agent` skill.

Evening task:
1. Read `data/today_shortlist.csv` and `data/internship_tracker.csv`.
2. Produce tomorrow's application plan with A/B/C priorities.
3. Separate roles into:
   - A_APPLY_NOW: apply immediately.
   - B_APPLY_SOON: verify then apply within 48 hours.
   - C_MASS_APPLY: useful for broad application volume.
   - D_LOW_PRIORITY: likely ignore.
4. Identify which companies need manual verification of date, duration, and apply link.
5. Suggest tracker updates but do not overwrite user-entered application statuses.
6. If scoring problems are visible, propose a patch but ask before making major changes.
7. Preserve user goal: internship offer probability for Aug-Nov 2026 is more important than salary.
