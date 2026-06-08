# Akira v2 Default Runtime Fix

## Purpose

Make `version_2_poisonous` the default playable Akira.

`version_1_cold` remains in the repository as legacy/cold backup, but normal play should not default to it.

## Changes

- API version: `3.5.6`
- `state_templates/current_state.json` now starts Akira with:
  - `runtime_variant: version_2_poisonous`
  - `behavior_version: version_2_poisonous`
  - `active_mask: version_2_poisonous`
  - story flag `akira_runtime_variant: version_2_poisonous`
- `runtime/characters/characters_runtime_index.yaml` marks v2 as default and v1 as legacy backup.
- Added `gpt/locks/akira_v2_default_lock.md`.
- turn-contract returns `akira_default_runtime: version_2_poisonous`.
- Required checks now treat v2 as default, not conditional.

## After upload

1. Commit directly to main.
2. Wait for Railway deploy.
3. Check `/health`: version should be `3.5.6`.
4. Update Actions schema.
5. Start a new chat/session.

Old sessions that already stored v1 may need a fresh session or an explicit message: `Акира версия 2`.
