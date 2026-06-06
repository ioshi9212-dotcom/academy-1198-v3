# Academy 1198 v3 — No Stub Scene Quality Fix

## Why

After the last fix GPT started showing intermediate loading text:
- "session created"
- empty header
- "need to collect turn contract"

This fix closes that loophole.

## What changed

- Adds `scene_quality_gate_contract` into `scene_contract`.
- Adds `engine/scene_quality_gate.md`.
- Strengthens response format and density contract.
- Keeps previous fixes: compact runtime summaries, Akira v1/v2, header split, session_id guard, save layer fix.

## Upload to GitHub

Upload all files with folders. Main file:

```text
app/main.py
```

Also upload:

```text
engine/scene_quality_gate.md
gpt/custom_gpt_instructions_NO_STUB_COMPACT.md
```

## After deploy

1. Wait Railway Success.
2. Update Actions schema:
   https://web-production-cd472.up.railway.app/openapi-actions.json
3. Replace Custom GPT Instructions with:
   `gpt/custom_gpt_instructions_NO_STUB_COMPACT.md`

## Expected behavior

In play mode GPT may only output:
1. exact failure line; or
2. complete scene.

No intermediate technical text.
