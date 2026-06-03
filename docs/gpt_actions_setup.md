# GPT Actions Setup

Use this endpoint as schema:

```text
https://your-service.up.railway.app/openapi-actions.json
```

## Required flow

1. At the beginning of every new ChatGPT chat, call `createSession`.
2. Store returned `session_id` only inside the current chat.
3. For every turn in this chat, call `getSessionTurnContract` with this `session_id`.
4. After every meaningful scene, call `applyTurnResult`.
5. If `needs_compaction=true`, call `compactSessionMemory`.

## Never

- Do not reuse `session_id` from another chat.
- Do not use test session as gameplay session.
- Do not search for the latest session automatically.
- Do not continue old session unless the user explicitly provides its `session_id`.

## Never

- Do not continue a new game from an old `session_id`.
- Do not use old chat memory instead of runtime state.
- Do not save hidden lore as NPC knowledge unless revealed in scene.
