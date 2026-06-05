# Patch: Turn Contract Compact Default

## Problem

The Action call is now correct about `user_input`, but it still sends:

```json
{
  "include_file_contents": true
}
```

That makes `getSessionTurnContract` return too much data and GPT Actions fails with:

```text
ResponseTooLargeError
```

## Fix

For normal play turns, the GPT should use:

```json
{
  "user_input": "начнем",
  "mode": "play",
  "include_file_contents": false
}
```

The API already returns `scene_contract`, which is the compact smart scene source.

## Files in this patch

```text
app_main_compact_default.diff
custom_gpt_instruction_hotfix.md
PATCH_README_TURN_CONTRACT_COMPACT.md
PATCH_MANIFEST_TURN_CONTRACT_COMPACT.json
```

## Apply

### Required code change

In `app/main.py`, change:

```python
class TurnContractRequest(BaseModel):
    user_input: str
    mode: Literal["play", "technical", "audit", "transfer"] = "play"
    include_file_contents: bool = True
```

to:

```python
class TurnContractRequest(BaseModel):
    user_input: str = ""
    mode: Literal["play", "technical", "audit", "transfer"] = "play"
    include_file_contents: bool = False
```

### Required Custom GPT instruction change

Use `custom_gpt_instruction_hotfix.md`.

## After deploy

1. Redeploy Railway.
2. Update GPT Actions schema from:

```text
/openapi-actions.json
```

3. Start a new session.
4. Test `начнем`.

Expected behavior:

- `createSession` succeeds.
- `getSessionTurnContract` succeeds with compact response.
- GPT uses `scene_contract`.
- No `ResponseTooLargeError`.
