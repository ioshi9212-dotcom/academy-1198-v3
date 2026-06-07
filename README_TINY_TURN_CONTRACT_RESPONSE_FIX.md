# Tiny Turn Contract Response Fix — 3.5.3

## Problem

`getSessionTurnContract` worked after the route fix, but the response was too large for GPT Actions.
Actions returned:

```text
ResponseTooLargeError
```

The main reason was duplication:

- top-level `turn_contract_classic_v2` contained the useful data;
- `scene_contract` bridge duplicated most of the same data again.

## Fix

Version `3.5.3` keeps the main classic contract, but returns a much smaller response:

- `scene_contract` is now tiny:

```json
{
  "version": "scene_contract_classic_bridge_v2_tiny",
  "usable": true,
  "source_contract_version": "turn_contract_classic_v2"
}
```

- no full classic contract duplication inside `scene_contract`;
- `character_runtime_focus` is trimmed;
- `day_contract.current_day_block` is trimmed;
- `knowledge_table` and `relationship_focus` are trimmed;
- `current_state` is tiny;
- `required_files` is limited to 30 paths.

## Expected after deploy

1. `/health` shows `3.5.3`.
2. `getSessionTurnContract` no longer returns `ResponseTooLargeError`.
3. Response has:

```text
contract_version: turn_contract_classic_v2
response_profile: tiny_3_5_3
scene_contract.version: scene_contract_classic_bridge_v2_tiny
scene_contract.usable: true
```

## After upload

1. Commit directly to main.
2. Wait Railway deploy.
3. Update Actions schema.
4. Start a fresh chat/session.
