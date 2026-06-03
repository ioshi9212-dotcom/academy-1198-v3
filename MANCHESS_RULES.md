# ManChess Rules

## Purpose

This repository is a plotted interactive novella engine. It is not a household simulator and not free improvisation.

## Source split

- GitHub stores canon, rules, templates and API code.
- Railway Volume stores live sessions and runtime state.
- GPT Actions is only a bridge to the runtime API.

## Scene law

Every scene must move at least one line: character, conflict, relationship, knowledge, reputation, training, calendar, open thread, or future-lock pressure.

## Anti-telepathy law

NPCs speak from their own knowledge, not from author files. Hidden lore is not NPC knowledge.

## Player control law

Akira is controlled by the player. The engine may describe visible body reactions and consequences, but not force Akira's decisions, important emotions, trust, forgiveness, romance, or replies.

## Session law

Every new ChatGPT chat must create a new runtime session before play starts.

Runtime state lives under:

```text
/data/sessions/{session_id}/state/
```

A new chat must never reuse a `session_id` from memory, previous chats, examples, tests, docs, or the latest folder in `/data/sessions`.

Old sessions can be resumed only when the user explicitly gives a concrete `session_id` and asks to continue that exact session.

No game should use shared `/data/state` as active memory.

See also: `engine/session_policy.md`.
