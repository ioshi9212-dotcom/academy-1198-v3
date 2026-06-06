# Scene Assembly Gate

## Purpose

This file is a hard runtime gate for play-mode scene generation.

The engine may not write a play scene until the minimum scene assembly packet is present and usable.

API, Actions, state, context, contract, debug and loading messages are internal. They must never be shown inside a play response.

## Hard rule

Before every play-scene answer, verify that the engine has enough data to assemble the scene.

A play scene may be written only after these pieces are available:

1. `current_state`
2. `scene_contract`
3. `scene_contract.current_frame`
4. `scene_contract.current_frame.header_values`
5. `scene_contract.header_contract`
6. `scene_contract.response_format_contract`
7. `scene_contract.scene_density_contract`
8. `scene_contract.character_load_plan.full_character_ids`
9. `scene_contract.character_slice` for every full/active/nearby character
10. `behavior` and `voice` for every full/active/nearby character
11. `scene_contract.relationship_slice`
12. `scene_contract.knowledge_slice`
13. `scene_contract.character_memory_slice`
14. `scene_contract.npc_autonomy_contract`
15. `scene_contract.relationship_behavior_contract`
16. `scene_contract.memory_write_contract`
17. `scene_contract.event_engine_slice`

If any critical item is missing, empty, too large to inspect, or unavailable because Action failed, do not write the scene.

## No fallback

Forbidden fallback phrases and behavior:

- "контракт слишком большой, беру точечно"
- "восстанавливаю формат вручную"
- "беру состояние по памяти"
- "у меня уже есть стартовое состояние"
- "нашла минимум"
- "сейчас исправлю сцену"
- "мой косяк"
- writing from chat memory
- writing from approximate remembered format
- writing a simplified scene because the contract is too large
- exposing any API/Action/debug/context/contract text to the user

If the engine cannot see the required packet, it must stop with the exact failure line.

## Exact failure line

Use exactly:

```text
Не удалось собрать scene assembly packet через Action. Без него я не продолжаю игровую сцену.
```

No extra explanation in play mode.

## Scene assembly order

Once the required packet is present:

1. Read `header_values`.
2. Build the emoji header exactly from `header_contract`.
3. Read active/full character behavior and voice from `character_slice`.
4. Read relationship state and behavior_next from `relationship_slice`.
5. Read character personal memory from `character_memory_slice`.
6. Read who knows what from `knowledge_slice`.
7. Select the current pressure from calendar/event_engine/open_threads.
8. Write the scene through visible POV only.
9. Stop at a real intervention point.
10. Add action choices, speech choices and true thoughts.
11. Prepare meaningful state updates for `applyTurnResultSimple`.

## Mandatory output format

A play response must have this exact shell:

```text
━━━━━━━━━━━━━━━━━━━━
📅 Дата:
🕒 Время:
📍 Место:
🌤 Погода:
🫀 Состояние Акиры:
🎒 При себе / рядом:
━━━━━━━━━━━━━━━━━━━━

[SCENE BODY]

━━━━━━━━━━━━━━━━━━━━
Что можно сделать:
1.
2.
3.

Что сказать:
— “...”
— “...”
— “...”

Мысли Акиры:
— ...
— ...
— ...
━━━━━━━━━━━━━━━━━━━━
```

Rules:

- Do not replace the choice block with "Что делает Акира?"
- Do not use a boxed title header.
- Do not use freeform date/location title formatting.
- Do not omit action options.
- Do not omit speech options.
- Do not omit thoughts.
- Thoughts must be short, true, POV-safe and practical.

## Partial success rule

A careful player action is not automatic full success.

If Akira acts carefully, the scene may reduce danger, hide power, avoid escalation or pass a check, but the world still reacts if there is visible pressure.

Examples:

- Minimal energy output can hide space, but staff may notice unusual control.
- Quiet compliance can pass the check, but a staff member may remember her face.
- Ignoring a provocation can avoid a fight, but the provoker may try again later.
- No alarm does not mean no consequence.
- "Nobody noticed" is allowed only if the scene has another meaningful consequence.

## Anti-null scene rule

Never end a meaningful scene with:

- "nothing happened"
- "no one noticed"
- "everything stayed stable"
- "the flow continued normally"
- "you may observe"
- "control is purely technical"

Unless there is another concrete trace:

- access changed
- note recorded
- rumor started
- relationship changed
- knowledge changed
- staff attention changed
- character memory updated
- open thread created
- event seed created
- next beat advanced

## Relationship behavior rule

Relationship state must affect NPC behavior.

Use:

- trust
- tension
- respect
- curiosity
- jealousy
- resentment
- private_status
- behavior_next
- triggers
- last_interaction
- shared_incidents

NPC behavior must be shaped by this data before scene writing.

If a relationship is empty but characters are old friends, use character files and initial knowledge, then save a relationship entry after the scene.

## Knowledge rule

Characters can act only on:

- what they saw
- what they heard
- what they were told
- what character files establish as prior knowledge
- what they can infer from visible signs

A player's private thought does not become NPC knowledge.

Hidden lore does not become NPC knowledge.

## Important line memory

Save only important lines, not all dialogue.

Save a line if it:

- changes relationship direction
- reveals a boundary
- creates a nickname, insult, promise, threat, debt or hook
- is likely to be remembered by an NPC
- publicly affects reputation
- exposes a character pattern
- causes jealousy, resentment, respect, curiosity or tension
- will matter in a future scene

Do not save routine filler lines.

## Self-check before sending

Before sending any play answer, silently verify:

- Header shell is correct.
- No technical/meta/debug text is visible.
- Scene has pressure.
- Scene does not nullify previous pressure.
- Active characters show character-specific behavior.
- NPCs do not obey player intent automatically.
- Relationships and knowledge were used.
- The scene leaves at least one trace.
- The ending block is complete.
