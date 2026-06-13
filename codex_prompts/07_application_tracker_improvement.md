# Prompt 07 — Application Tracker Improvement

Use `AGENTS.md` and the `malaysia-da-internship-agent` skill.

Task:
1. Improve `data/internship_tracker.csv` structure without overwriting user-entered statuses.
2. Preserve columns such as Applied, Interview, Offer, Rejected, Remarks if they already exist.
3. Add useful fields if missing:
   - application_date
   - status
   - next_action
   - follow_up_date
   - interview_date
   - contact_person
   - notes
4. Ensure tracker update logic merges by stable job_id and does not duplicate rows unnecessarily.
5. Add clear recommended actions from buckets.
6. Validate with dry-run and inspect CSV diff.
