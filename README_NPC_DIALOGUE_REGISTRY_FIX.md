# NPC Dialogue + Registry Fix

## What it fixes

The model was turning NPC pressure into abstract narration only.

Example bad pattern:

`Одна девушка впереди пытается возмутиться...`

The old repo used stronger social dynamics: NPCs are not background only. They should speak, argue, provoke, interrupt, and create opportunities for Akira to intervene.

## Added

- `npc_dialogue_contract` in tiny turn-contract response.
- `npc_registry_contract` in tiny turn-contract response.
- `gpt/locks/npc_dialogue_intervention_lock.md`.
- `npc_registry_changes` support in `applyTurnResult`.
- `npc_registry_changes_json` support in `applyTurnResultSimple`.
- `state_templates/npc_registry.json`.

## Expected behavior

Public/social pressure should usually include at least one direct NPC line.

If an NPC becomes important:
- name;
- role;
- conflict;
- secret;
- relationship impact;
- return hook;

save them to `npc_registry.json`.

## After upload

1. Commit directly to main.
2. Wait Railway deploy.
3. `/health` should show `3.5.4`.
4. Update Actions schema.
5. Start a fresh session.
