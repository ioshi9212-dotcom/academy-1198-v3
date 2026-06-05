# Compaction Policy

## Trigger

Memory compaction runs every 15 meaningful game turns.

The counter is stored in:

```text
/data/sessions/{session_id}/state/compaction_state.json
```

## Purpose

Compaction keeps the game playable without erasing consequences.

It must preserve:

- revealed names;
- meaningful relationship changes;
- knowledge changes;
- promises;
- debts;
- meetings;
- conflicts;
- injuries;
- items;
- reputation shifts;
- important quotes;
- resolved but important threads;
- character-specific memory perspective.

It may remove or shorten:

- repeated empty movement;
- duplicated descriptions;
- routine travel without consequence;
- completed minor logistics;
- repeated food/sleep actions with no story function.

## Resolved threads

Resolved threads are not deleted immediately.

They move through this path:

```text
open -> resolved -> compacted memory
```

A resolved thread may be removed from active open threads only after its consequence is saved in one of:

- relationships;
- character memory;
- compacted scene history;
- reputation state;
- inventory state.

## Compaction output

After compaction, update:

- `recent_turns.md`;
- `open_threads.json`;
- `relationships.json`;
- `character_memory/*.json`;
- `shared_incidents.json`;
- `scene_history_compacted.md`;
- `compaction_state.json`.
