# Fix summary — academy-1198-v3

## Critical runtime problem fixed

Before fix:

- templates stored runtime data inside containers like `relationships`, `character_knowledge`, `threads`, `incidents`, `items`;
- `app/main.py` read many of these files as if items were on the top level;
- `applyTurnResultSimple` silently converted invalid JSON to `{}`.

Result: scenes could lose relationships, NPC knowledge, open threads and incident continuity.

After fix:

- reads support container format and old top-level legacy format;
- writes normalize new patches into the correct containers;
- invalid JSON produces explicit API error.

## Expected behavior improvement

- Characters should remember focused relationship dynamics.
- Open threads should come back into `scene_contract`.
- Shared incidents should stop disappearing.
- Event seeds/queue should be visible to the event engine.
- Bad state updates should fail loudly instead of pretending nothing happened.

## Files changed

- `app/main.py` via patch/script.
- `engine/source_priority.md`
- `engine/current_frame_policy.md`
- `engine/loading_policy.md`
- `gpt/engine_prompt.md`
- `characters/raiden/*`
- `state_templates/event_seeds.json`
- `state_templates/event_queue.json`
