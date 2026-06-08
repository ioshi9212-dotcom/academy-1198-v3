# 3.6.0 Natural Flow + Short Custom GPT Instructions

## Version

API: `3.6.0`

## Fix

The game started drifting into procedural micro-steps:
- approach desk;
- look at panel;
- take card;
- wait instruction;
- walk two steps.

This fix adds `action_flow_contract` and strengthens `scene_progress_contract`.

## New behavior

The model must aggregate obvious action chains:

- registration/check -> result + consequence + next route/pressure;
- coffee -> take coffee + social beat;
- corridor -> move to next meaningful interruption;
- minimal energy response -> brief signal result + staff/NPC/social consequence.

Stop only at a real choice:
- reply/silence;
- obey/challenge/bypass;
- hide/show/risk;
- protect/cut off/let NPC handle;
- intervene/ignore/use distraction.

## Short Custom GPT Instructions

Use:

`gpt/CUSTOM_GPT_INSTRUCTIONS_UNDER_8000_v3_6_0.md`

It is under 8000 characters and includes:
- session rule;
- play gate;
- source rules;
- natural flow / action aggregation;
- emoji header/separators;
- Akira start outfit/items;
- save rules;
- technical mode.

## Schema

After deploy update Actions schema from:

`https://web-production-cd472.up.railway.app/openapi-actions.json`

## After upload

1. Upload ZIP to GitHub.
2. Commit directly to `main`.
3. Wait Railway deploy.
4. `/health` should show `3.6.0`.
5. Update Actions schema.
6. Copy the short instruction text into Custom GPT Instructions.
7. Start a new session.
