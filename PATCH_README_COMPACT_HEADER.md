# Patch: Compact Contract + Header Contract

## Purpose

This patch fixes the current working chain without touching lore.

It fixes:

1. `ResponseTooLargeError` risk:
   - `TurnContractRequest.include_file_contents` now defaults to `false`.
   - `user_input` now has a safe default `""`.

2. Scene header format:
   - Adds `scene_contract.header_contract`.
   - Adds `scene_contract.current_frame.header_values`.
   - Gives GPT ready human strings for:
     - date;
     - time;
     - location;
     - weather;
     - POV state;
     - short carried/nearby context.

3. Location display:
   - Replaces `Academy Main` with Russian header names.

4. File reading:
   - Keeps old path endpoint.
   - Adds safer query endpoint:
     - `GET /api/v1/file?path=engine/output_format.md`
   - Exposes it in OpenAPI as `getProjectFileByQuery`.

5. GPT instruction:
   - Updates repository instruction to use compact contract by default.
   - Removes outdated full-contract-first flow.

## Files

```text
app/main.py
engine/output_format.md
world/locations/academy_main/location_card.yaml
gpt/custom_gpt_instructions.md
PATCH_README_COMPACT_HEADER.md
PATCH_MANIFEST_COMPACT_HEADER.json
```

## Upload

Unzip into repository root and replace files.

Recommended commit:

```text
Fix compact turn contract and scene header
```

## After upload

1. Wait for Railway redeploy.
2. Check:

```text
/health
```

Expected:

```text
version: 3.1.1
```

3. Update GPT Actions schema from:

```text
/openapi-actions.json
```

4. Start a new session or reset existing session.

## Important

For normal play calls, GPT must call:

```json
{
  "user_input": "начнем",
  "mode": "play",
  "include_file_contents": false
}
```

Do not use `include_file_contents=true` for normal gameplay.
