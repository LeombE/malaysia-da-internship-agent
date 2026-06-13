# Prompt 03 — V3 Telegram + Dedup + Official Source Priority

Use `AGENTS.md` and the `malaysia-da-internship-agent` skill.

Implement V3 carefully:

1. Add Telegram notification for high-value jobs only:
   - `A_APPLY_NOW`
   - high-confidence `B_APPLY_SOON`
   - avoid spamming all `C_MASS_APPLY` roles.
2. Telegram secrets must come from environment variables / GitHub Secrets:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   Do not hardcode or print them.
3. Improve deduplication:
   - Group likely duplicates by normalized title + company + state.
   - Prefer official career / ATS apply URLs over aggregators.
   - Preserve all raw source references if useful, but output the best apply URL.
4. Improve source scoring:
   - Official company career page: meaningful bonus.
   - ATS links: meaningful bonus.
   - Mainstream job boards: small bonus or neutral.
   - Aggregators: modest penalty, not deletion.
5. Update CSV output columns if needed, but preserve backwards compatibility where possible.
6. Add tests or dry-run validation.
7. Update README or `README_V2_OPTIMIZATIONS.md` with V3 notes.
8. Run a quota-safe local dry-run before commit.
9. Confirm `.env` and `.venv` are not staged.

Return a changelog, validation output, and any GitHub Secret names I must add manually.
