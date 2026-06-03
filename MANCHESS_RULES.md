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

Every new run creates a new session. Runtime state lives under `/data/sessions/{session_id}/state/`. No game should use shared `/data/state` as active memory.
