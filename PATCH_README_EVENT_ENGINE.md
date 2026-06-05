# Patch: Academy Event Engine + Director Notes

## Purpose

This patch adds the missing scene engine layer.

Calendar gives major points.

Event Engine creates interesting scenes between them:

- gossip;
- jealousy;
- rating pressure;
- provocations;
- minor fights;
- energy flares;
- social glances;
- instructor notes;
- delayed character entries;
- small mistakes with consequences;
- future hooks.

The goal is to stop the game from feeling like a registration checklist.

## Files

```text
app/main.py
engine/event_engine_rules.md
engine/scene_generation_rules.md
engine/output_format.md
gpt/custom_gpt_instructions.md
state_templates/event_seeds.json
state_templates/event_queue.json
state_templates/director_notes.json
state_templates/gossip_state.json
state_templates/rating_state.json
state_templates/energy_incidents.json
PATCH_README_EVENT_ENGINE.md
PATCH_MANIFEST_EVENT_ENGINE.json
```

## What changes in API

API version becomes:

```text
3.2.0
```

`scene_contract` now includes:

```text
event_engine_slice
```

`applyTurnResult` and `applyTurnResultSimple` can save:

```text
event_seed_changes
event_queue_changes
director_note_changes
gossip_changes
rating_changes
energy_incident_changes
```

For `applyTurnResultSimple`, use JSON string fields:

```text
event_seed_changes_json
event_queue_changes_json
director_note_changes_json
gossip_changes_json
rating_changes_json
energy_incident_changes_json
```

## Upload

Unzip into repository root and replace files.

Recommended commit:

```text
Add academy event engine and director notes
```

## After upload

1. Wait for Railway redeploy.
2. Check:

```text
/health
```

Expected:

```text
version: 3.2.0
```

3. Update GPT Actions schema from:

```text
/openapi-actions.json
```

4. Start a new session or reset existing session.

## Important

Old sessions will not automatically get the new state template files unless reset/new session is created.
