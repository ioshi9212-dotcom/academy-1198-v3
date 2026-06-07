# Academy 1198 v3 — Classic Turn Contract Restore

## Why

The previous v3 architecture became too heavy:

- full scene_contract caused ResponseTooLargeError;
- ultra compact fixed size but made scenes short/dumb;
- balanced compact helped but still made the model serve contracts instead of directing scenes.

The older repository worked better because the API returned a simple turn-contract:

- active characters;
- nearby/focus characters;
- required files;
- output format;
- allowed/forbidden facts;
- checks;
- knowledge;
- inventory;
- canon locks.

This package restores that pattern.

## Main change

`getSessionTurnContract` now returns:

```text
contract_version: turn_contract_classic_v2
```

Primary fields are top-level:

```text
active_character_ids
nearby_character_ids
focus_character_ids
required_files
output_format_contract
allowed_new_facts_this_turn
forbidden_new_facts_this_turn
required_checks_before_answer
knowledge_table
inventory_contract
canon_locks
day_contract
relationship_focus
character_runtime_focus
```

`scene_contract` remains only as a tiny backward-compatibility note.

## Preserved fixes

This restore keeps:

- session_id guard;
- save layer fix;
- Akira v1/v2 split;
- Akira v2 voice rules;
- Livia voice rules;
- markdown dialogue format;
- no micro-choice rule;
- academy energy background;
- 15 Aug no automatic Akira energy check;
- 31 Aug energy privacy;
- factual prose rules.

## Upload

Upload all files preserving folders. Commit directly to `main`.

Because `app/main.py` changed, after Railway deploy update Actions schema:

https://web-production-cd472.up.railway.app/openapi-actions.json

Replace Custom GPT Instructions with:

```text
gpt/custom_gpt_instructions_CLASSIC_RESTORE.md
```

## First test prompt

In a fresh chat:

```text
Начнем. Акира версия 2.
```

Expected:
- no technical commentary;
- contract_version is classic internally;
- scene is not short;
- format is correct;
- Livia active;
- no automatic Akira energy clarification on registration.
