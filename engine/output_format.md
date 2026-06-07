# Output Format

This file is the strict response format for play scenes.

## Priority

This format has highest priority for scene output. If the answer is not in this format, rewrite it before sending.

## Allowed play response parts

A play response contains only:

1. emoji header;
2. scene body;
3. choice block;
4. speech options;
5. POV thoughts.

No assistant commentary before or after the scene.

## Header

Every play scene starts with this emoji header format:

```text
📅 15 августа сб 1198
🕒 Утро, около 08:40
📍 Место: Академия Астрейн, входная зона
🌤 Погода: переменная облачность, 22°C
🫀 Состояние Акиры: собрана
🎒 При себе / рядом: толстовка, джинсы, сумка с одеждой, документы, телефон, волосы распущены, Ливия
```

Use values from `scene_contract.current_frame.header_values`, `scene_contract.header_contract`, and `current_state`.

## Scene body

Scene body is written through visible POV.

Use 7-12 short paragraphs/units for a meaningful scene. Do not stop after pure scenery. Do not write procedural registration explanation.

## Markdown body format

Descriptions, actions, atmosphere and system reactions go as separate italic paragraphs:

```text
*Поток новичков сужается у стоек сверки. На экранах мигают номера секций.*
```

Dialogue format is strict:

```text
**Имя или видимый дескриптор** — Реплика. (*короткая ремарка: тон, взгляд, пауза, жест*)
```

Rules:

- speaker name/descriptor is always bold;
- use a long dash after speaker;
- dialogue text is plain;
- stage note is optional, short, in parentheses and italic;
- do not put long actions in parentheses;
- do not put thoughts in parentheses;
- if POV does not know a name, use a visible descriptor.

Correct:

```text
**Ливия** — Я могу устроить сцену. (*тихо, быстро глядя на сотрудницу*)
```

```text
*Браслет у соседнего новичка мигнул один раз. Сотрудница у стойки назвала его фамилию, и он убрал руку от стакана.*
```

Wrong:

```text
Ливия: Я могу устроить сцену.
Ливия — Я могу устроить сцену. [смотрит на сотрудницу]
Браслет у соседнего новичка мигнул один раз.
```

## Known names

Use known names only when POV already knows them. Otherwise use visible descriptors:
`рыжий студент`, `девушка с планшетом`, `сотрудник сверки`.

## POV and first person

Narration may say "Акира" because scene is third-person visible POV.

But bottom options and thoughts must be written as POV options.

Use first person for inner stance:

Correct:
`думать, что я послушная`

Wrong:
`думать, что Акира послушная`

Physical action options can stay infinitive:
`пройти к стойке`, `остаться у окна`, `подойти к Ливии`.

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

Use 2-4 action options and 2-4 short speech options.

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
- descriptions are italic separate paragraphs;
- dialogue uses bold speaker + long dash;
- stage notes are short, italic and in parentheses;
- no NPC thoughts as facts;
- no direct POV thoughts inside scene body;
- bottom choices/thoughts do not use third-person inner stance.
