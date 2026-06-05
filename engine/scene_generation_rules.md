# Scene Generation Rules

## Purpose

A scene must move at least one line:

- relationship;
- conflict;
- knowledge;
- training;
- reputation;
- calendar;
- open thread;
- access;
- schedule;
- world pressure;
- physical state;
- clothing state;
- weather consequence;
- future setup;
- character boundary.

If it moves none of these, summarize the routine and move to the next meaningful moment.

## Meaningful scene density

A meaningful scene should contain 3-5 scene beats.

Minimum beats:

1. **Motion** — something in the environment or Academy system is happening.
2. **POV observation** — the POV character notices concrete details without needing the player to ask every time.
3. **Active presence** — active/nearby characters have visible presence, reaction, movement or dialogue.
4. **Pressure/change** — a rule, schedule, access point, social reaction, conflict, reputation signal, body state or relationship changes.
5. **Intervention point** — the scene stops where the player has a real action or line.

Do not end the scene immediately after setting decoration.

## Active characters

Use `current_state.active_character_ids`.

Active characters must matter in the scene unless state or a scene event removes them.

Do not silently move active characters away.

`mentioned_character_ids` are references, not presence.

`scheduled_character_ids` and `delayed_character_ids` are future pressure, not automatic current speakers.

## Calendar use

Use `scene_contract.calendar_slice.current_day_block`.

Do not read the whole calendar as today's active scene.

Use the current day event as pressure and direction, not fixed prose.

Beats are order and purpose, not text to copy.

## Character file use

Full character files are for POV/active/nearby.

Mentioned/scheduled/delayed characters use light info unless they enter the scene.

If a character enters the scene, they become active/nearby and their full files are needed next turn.

## Relationships and knowledge

Use `scene_contract.relationship_slice`, `knowledge_slice`, `open_threads_slice`, and `shared_incidents_slice`.

Do not use all relationships or all knowledge as if every NPC knows everything.

If a character is not present and not directly relevant, their relationship data should not drive the current scene.

## Time and weekday

Track date, day of week, time and time of day.

When date advances, day of week advances too.

## Weather

Every scene header includes current weather.

Weather affects the scene when relevant: rain wets clothes and ground; wind affects hair and sound; heat affects fatigue; cold affects breath and fingers.

## Physical continuity

Actions affect body and state. Wet clothes, pain, injuries, fatigue, hunger, thirst, changed hair and damaged clothing persist until fixed.

## Player and POV character

The player controls the POV character's actions.

The character remains a character, not an empty doll.

If the player chooses something against the character's habits, body state or boundaries, the action can happen, but the scene may show hesitation, discomfort, irritation, delayed reaction, inner disagreement in thoughts, relationship consequence or body-state consequence.

Do not block the action only because the character dislikes it.

Block or modify only if physically impossible, current state prevents it, scene context makes it impossible, or it violates established facts.

## Time flow

Do not move time by tiny increments without reason.

Short scene: time may not change. Dialogue/check/queue: +10 to 40 minutes. Location transfer: +5 to 30 minutes. Training, medical check, sparring, instruction: +30 minutes to 3 hours.

## Time skip

Before skipping time, check current calendar day/event, blocking events, open threads, promises, character availability, unresolved consequences, body/clothing state, injuries and fatigue.

If nothing meaningful exists, summarize the gap and stop at the next meaningful moment.
