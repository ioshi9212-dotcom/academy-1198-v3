# Current Frame Policy

## Active project

The active project is `academy-1198-v3`.

The active runtime frame is Academy 1198:

- `current_year`: `1198`
- `current_calendar_id`: `academy_start`
- `current_date`: `1198-08-15`
- `current_day_id`: `academy_day_001`
- `current_location_id`: `loc_academy_main`
- `current_arc_id`: `arc_001_academy_start`
- `pov_character_id`: `char_akira`

## Source priority

Use `engine/source_priority.md` as the only source-priority law.

Short form:

1. latest explicit user correction;
2. runtime session state;
3. recent turns / scene history / compacted memory;
4. current `academy-1198-v3` files;
5. current calendar / arc / active loaded character files;
6. focused knowledge, memory, relationships and incidents;
7. old canon and prequel as reference only.

Direct current user correction beats stale repo text. Runtime state beats old canon.

## Calendar

The calendar is a canon guide for meaningful events.

It is not a command to write every day.
It is not permission to skip open threads.
It is not a replacement for current state.

If the player requests a time skip, the engine moves to the nearest meaningful event after checking:

- required calendar events;
- blocking events;
- open threads;
- due promises and meetings;
- character availability;
- unresolved consequences;
- Akira's physical and energy state.

## Academy frame

Academy scenes should feel like a living institution:

- schedules;
- checks;
- instructors;
- student noise;
- reputation;
- rankings;
- permissions;
- access limits;
- training;
- dormitory life;
- social pressure;
- consequences.

The Academy is not a cozy school, not a prison, and not a static registration desk.

## Scene frame use

For a normal play turn, use `scene_contract.current_frame` first.
Do not replace the frame with old memory or with general project lore.
