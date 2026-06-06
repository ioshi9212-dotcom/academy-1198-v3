# Runtime Character Slice Rules

Normal play turns must use compact runtime summaries instead of full `behavior.md` and `voice.md`.

## Why

Full behavior/voice files are canon sources, but they are too large for every Action response.
The scene contract must stay compact enough to load reliably.

## Runtime summary rule

For every full/active/nearby character, `scene_contract.character_slice` should include:

- `runtime_summary` from `runtime/characters/{folder}.yaml`;
- a small `card_hint`;
- optional small `goals_hint` only when the character drives the scene;
- optional small `detail_hint` only for energy/training/combat/past/medical/close interaction scenes.

Do not include full behavior/voice text in normal play.

## Fallback

If runtime summary is missing, use only a tiny fallback from behavior/voice:

- behavior max about 900 chars;
- voice max about 700 chars.

Then the engine should still prefer creating/fixing the runtime summary file.

## Character integrity

Runtime summaries must preserve:

- core behavior;
- scene behavior;
- voice rhythm;
- relationship hooks;
- forbidden mistakes;
- memory hooks.

A summary is not a replacement for canon. It is the combat-ready slice used during play.
