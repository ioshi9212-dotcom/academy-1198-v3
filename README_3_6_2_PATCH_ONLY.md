# 3.6.2 PATCH ONLY

This is a small patch, not a full project snapshot.

## Fixes

1. Keeps GPT in novel runtime-director mode.
2. Uploaded images are visual references only unless the user explicitly asks image work.
3. Strengthens `compact_output_format_for_response()` so Action response includes:
   - separator line;
   - exact emoji header template;
   - exact ending template;
   - hard rule not to collapse choice block into one line.
4. Adds top-level `header_contract`.
5. Adds one active short Custom GPT instruction file:
   `gpt/CUSTOM_GPT_INSTRUCTIONS_ACTIVE.md`

## Files included

- `app/main.py`
- `.github/workflows/classic-runtime-smoke.yml`
- `gpt/CUSTOM_GPT_INSTRUCTIONS_ACTIVE.md`
- `gpt/CUSTOM_GPT_INSTRUCTIONS_UNDER_8000_v3_6_2.md`
- `CLEANUP_DELETE_LIST_3_6_2.md`
- `PATCH_MANIFEST_3_6_2.json`

## After upload

1. Upload this ZIP to GitHub.
2. Commit directly to main.
3. Wait Railway deploy.
4. `/health` should show `3.6.2`.
5. Update Actions schema:
   `https://web-production-cd472.up.railway.app/openapi-actions.json`
6. Copy instructions from:
   `gpt/CUSTOM_GPT_INSTRUCTIONS_ACTIVE.md`
7. Start a fresh chat/session.

## Cleanup

Read `CLEANUP_DELETE_LIST_3_6_2.md`.
ZIP upload will not delete old files automatically.
