# Output Format

This file is the strict response format for play scenes.

## Priority

This format has highest priority for scene output.

If the answer is not in this format, rewrite it before sending.

## Allowed play response parts

A play response contains only:

1. emoji header;
2. scene body;
3. choice block;
4. speech options;
5. POV thoughts.

No assistant commentary before or after the scene.

Do not mention:

- scene saved;
- API;
- Actions;
- turn-contract;
- state;
- technical status;
- “you can continue” outside the in-world choice block.

## Header

Every play scene starts with this emoji header format.

Use values from:

- `scene_contract.current_frame.header_values`;
- `scene_contract.header_contract`;
- `current_state`.

```text
📅 19 августа пн 1198
🕒 Утро, около 10:38
📍 Место: Академия Астрейн, зона I-2 тренировочного блока
🌧 Погода: ясное августовское утро
🫀 Состояние Акиры: после воды дыхание ровное; ноги, плечи и руки устали, но состояние рабочее
🎒 При себе / рядом: пластина комнаты, ремень допуска D, телефон, резинка, экран инструктажа
```

## Header rules

Required lines:

1. `📅 {date_human}`
2. `🕒 {time_human}`
3. `📍 Место: {location_human}`
4. `🌤/🌧/☁️ Погода: {weather_human}`
5. `🫀 Состояние Акиры: {pov_state_human}`
6. `🎒 При себе / рядом: {context_human}` only if there is something useful to list.

Do not write English location names if a Russian header name exists.

Do not list absent items.

Keep the `🎒` line short.

If no relevant item/object/person is present, omit the `🎒` line.

## Scene body

Scene body is written through visible POV.

Use 3-5 scene beats and usually 5-9 short paragraphs/units for a meaningful scene:

1. environment or Academy system in motion;
2. what the POV character notices;
3. visible reaction/action from active or nearby characters;
4. pressure, conflict, rule, schedule, access, reputation, event seed or relationship movement;
5. stop point where the player can intervene.

Do not stop after pure scenery.

Do not write a scene that is only:

- weather;
- one decorative paragraph;
- “what does Akira do?” with no pressure;
- procedural registration explanation.

## Event engine in scene

Use event pressure when fitting:

- gossip;
- jealousy;
- rating;
- provocation;
- energy flare;
- minor fight;
- instructor attention;
- delayed character entry;
- social comparison.

Do not show the hidden director plan to the user.

## Descriptions

Descriptions, actions and atmosphere go as separate italic paragraphs.

```text
*Поток новичков сужается у стоек сверки. На экранах мигают номера секций, и каждая задержка сразу становится заметной.*
```

## Dialogue

Dialogue format is strict:

```text
**Имя или видимый дескриптор** — Реплика. (*короткая ремарка: тон, взгляд, пауза, жест*)
```

Rules:

- speaker name/descriptor is always bold;
- use a long dash after speaker;
- dialogue text is plain;
- stage note is optional and short;
- do not put long actions in parentheses;
- do not put thoughts in parentheses;
- if POV does not know a name, use a visible descriptor.

## Known names

Use known names only when POV already knows them.

Unknown character examples:

- `рыжий студент`;
- `девушка с планшетом`;
- `высокий тёмноволосый парень`;
- `сотрудник сверки`.

## Thoughts

Do not write direct inner thoughts inside the scene body.

Wrong:

```text
Акира подумала, что это слишком спокойно.
```

Right:

- show face, breath, pause, attention in the scene;
- put real thoughts only in the bottom block.

## Ending block

Every play scene ends with:

```text
━━━━━━━━━━━━━━━━━━━━
Что можно сделать:
1.
2.
3.

Что сказать:
— ""
— ""
— ""

Мысли Акиры:
—
—
—
━━━━━━━━━━━━━━━━━━━━
```

Use 2-4 action options.

Use 2-4 short speech options.

Options must match POV character.

For Akira:

- short;
- dry;
- observant;
- controlled;
- no polite default unless masking;
- no long explanation.

Thoughts must be short, concrete and in character.

## Self-check before sending

Before sending, check:

- emoji header exists;
- no assistant meta-commentary exists;
- header uses the exact line style from this file;
- date/day/time/location/weather came from state or scene_contract;
- location is not an English fallback if Russian name exists;
- active/nearby characters were not omitted without reason;
- body has 3-5 meaningful beats unless this is a pure transition;
- at least one scene pressure exists;
- if possible, event_engine_slice affected the scene;
- dialogue uses bold speaker + long dash;
- descriptions are italic separate paragraphs;
- no NPC thoughts as facts;
- no direct POV thoughts inside scene body;
- bottom blocks exist.
