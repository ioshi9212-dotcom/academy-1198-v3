# Output Format

This file is the strict response format for play scenes.

## Priority

This format has highest priority for scene output.

If the answer is not in this format, rewrite it before sending.

## Header

Every play scene starts with a short header.

```text
━━━━━━━━━━━━━━━━━━━━
📅 1198-08-15, суббота | 🕒 08:40
📍 Академия Астрейн, главный вход
☁️ Переменная облачность, +22°C, сухо
🫀 Акира: собрана, без травм
👥 Рядом: Ливия
━━━━━━━━━━━━━━━━━━━━
```

The exact values must come from `current_state` and `scene_contract.current_frame`.

## Header rules

Keep the header compact.

Required data:

- date + day of week + time;
- location;
- weather;
- short POV state;
- nearby/active characters only if they are actually present according to state.

Do not list absent items.

Bad:

```text
В руках ничего. В карманах ничего. Оружия нет.
```

Good:

```text
🎒 Сумка через плечо, документы новичка
```

If no relevant item is present, omit the item line.

## Scene body

Scene body is written through visible POV.

Use 3-5 scene beats for a meaningful scene:

1. environment or Academy system in motion;
2. what the POV character notices;
3. visible reaction/action from active or nearby characters;
4. pressure, conflict, rule, schedule, access, reputation or relationship movement;
5. stop point where the player can intervene.

Do not stop after pure scenery.

Do not write a scene that is only:

- weather;
- one decorative paragraph;
- "what does Akira do?" with no pressure.

## Descriptions

Descriptions, actions and atmosphere go as separate italic paragraphs.

```text
*Ветер тянет по двору запах влажного бетона и металла. Несколько студентов в бордовой форме задерживают взгляд на белых волосах Акиры.*
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

Thoughts must be short, concrete and in character.

## Self-check before sending

Before sending, check:

- header exists;
- header is short;
- date/day/time/location/weather came from state;
- active/nearby characters were not omitted without reason;
- body has 3-5 meaningful beats unless this is a pure transition;
- dialogue uses bold speaker + long dash;
- descriptions are italic separate paragraphs;
- no NPC thoughts as facts;
- no direct POV thoughts inside scene body;
- bottom blocks exist.
