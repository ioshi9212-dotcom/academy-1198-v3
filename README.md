# Academy 1198 v3

Clean ManChess-style novella engine skeleton.

## Core idea

- GitHub stores canon, rules, templates and API code.
- Railway Volume stores live runtime sessions.
- GPT Actions call the API and never play from stale memory.

## Start order

1. Deploy this repo to Railway.
2. Mount a Railway Volume at `/data`.
3. Set `NOVELLA_RUNTIME_DATA_ROOT=/data`.
4. Open `/openapi-actions.json` and use it as GPT Actions schema.
5. Create a new session before every new game run.

## Hard rule

This is a plotted interactive novella engine, not a household sandbox. Every scene must move character, conflict, knowledge, relationship, reputation, training, calendar, or future-lock pressure.
