# Scene Quality Gate

This is a hard gate for play-mode answer quality.

## Allowed play outputs

In play mode only two output types are allowed:

1. Exact failure line:
`Не удалось собрать scene assembly packet через Action. Без него я не продолжаю игровую сцену.`

2. Complete scene in the required format.

No third option.

## Strictly forbidden

Never show the user:
- "сессия создана";
- "контракт загружен";
- "нужно собрать turn contract";
- "сейчас начнём";
- empty/placeholder header;
- API/Action/state/debug/tool/loading commentary;
- a short scene stub;
- a one-paragraph summary.

## Minimum scene quality

A meaningful play scene must have:

- filled emoji header;
- 7-12 short paragraphs/units;
- environment/system in motion;
- Akira POV observation;
- at least one active NPC line or character-specific visible action;
- concrete pressure/change;
- world movement even if Akira acts calmly;
- real intervention point;
- choices tied to current pressure;
- speech choices in selected Akira version;
- thoughts in selected Akira version.

## Passive action rule

If user writes "идти спокойно" or another passive action, do not answer with a passive scene.

The world must advance:
- queue shifts;
- staff calls;
- screen changes;
- Livia reacts;
- someone notices;
- route narrows;
- gossip/attention starts;
- a delayed hook moves closer.

## Akira v2

For `version_2_poisonous`:
- thoughts are short, practical, poisonous;
- line options are not polite defaults;
- smile/tone is lazy-dangerous when relevant;
- no author summary.

Good examples:
- "Ливия сейчас громче стойки. Полезно. Почти."
- "Сотрудница смотрит на руки. Умная."
- "Пять минут. Уже кто-то хочет быть первым идиотом."
- "Я пока послушная. Наслаждайтесь редкостью."
