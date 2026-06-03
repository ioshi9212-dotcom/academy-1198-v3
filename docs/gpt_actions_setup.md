# GPT Actions Setup

Use this endpoint as schema:

```text
https://your-service.up.railway.app/openapi-actions.json
```

## Required flow

1. Before a new game, call `createSession`.
2. Store returned `session_id` for this chat/run.
3. For every turn, call `getSessionTurnContract`.
4. After every meaningful scene, call `applyTurnResult`.
5. If `needs_compaction=true`, call `compactSessionMemory` after summarizing the last turns into durable memory.

## Never

- Do not continue a new game from an old `session_id`.
- Do not use old chat memory instead of runtime state.
- Do not save hidden lore as NPC knowledge unless revealed in scene.
