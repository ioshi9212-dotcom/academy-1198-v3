# Full Scene Fix Patch — Academy 1198 v3

## Purpose

This is a full replacement patch for the current scene-quality problem.

It fixes the specific problems from the latest test:

1. Scenes still read like registration instructions.
2. GPT does not reliably fetch active characters' behavior/voice.
3. Livia sounds like a generic companion/guide instead of a close old friend.
4. Akira choices are too neutral.
5. Event Engine has no strong top-level novel priority.

## Files included

```text
app/main.py
engine/novel_director_core.md
engine/event_engine_rules.md
engine/scene_generation_rules.md
engine/output_format.md
gpt/custom_gpt_instructions.md
story/calendar/academy_start.yaml
state_templates/event_seeds.json
state_templates/event_queue.json
state_templates/director_notes.json
state_templates/gossip_state.json
state_templates/rating_state.json
state_templates/energy_incidents.json
PATCH_README_FULL_SCENE_FIX.md
PATCH_MANIFEST_FULL_SCENE_FIX.json
```

## Main changes

- Adds `engine/novel_director_core.md`.
- Adds it to `CORE_REQUIRED_FILES` before other scene rules.
- Forces active/full character behavior and voice usage.
- Tells GPT to fetch only `behavior.md` and `voice.md` for active/full characters when missing.
- Removes registration-heavy wording from the first day calendar.
- Seeds the first day with social attention, Livia social pressure, minor energy flicker and Kir delayed entry.
- Strengthens director notes.

## Recommended commit

```text
Apply full scene director fix
```

## After upload

1. Wait Railway redeploy.
2. Check `/health`.
3. Expected API version: `3.2.1`.
4. Update Actions schema from `/openapi-actions.json`.
5. Create a new session/reset old session.
