# NPC Dialogue Intervention Lock

## Problem

Do not turn living NPC pressure into abstract narration only.

Bad:
`Одна девушка впереди пытается возмутиться...`

Better:
`**Девушка у стойки** — Почему у меня снова другая секция? Я не буду третий раз стоять в этой очереди. (*голос срывается выше, чем она хотела*)`

Then show staff/crowd/system reaction.

## Rule

If a student, staff member, crowd member or temporary NPC creates visible pressure, give them direct dialogue or a concrete action.

Use visible descriptor if POV does not know the name.

Dialogue format:
`**Видимый дескриптор или имя** — Реплика. (*короткая ремарка*)`

## When NPC can stay background

NPC may remain pure background only if:
- they do not create pressure;
- they do not affect choice;
- they do not trigger rumor/reputation/relationship;
- Akira cannot realistically intervene.

## When NPC must become direct

Use direct NPC line/action when:
- they argue with staff;
- insult/provoke someone;
- show fear, pride, status, jealousy, curiosity;
- create social pressure around POV or companion;
- reveal a rule through conflict;
- trigger staff/system reaction;
- become possible return character.

## Akira interaction

Direct NPC scenes should create possible intervention:
- answer;
- ignore;
- cut in;
- let companion react;
- use the distraction;
- observe for information;
- make the NPC remember Akira.

## Save rule

If NPC gets a name, role, conflict, secret, relationship effect or likely return, save to `npc_registry.json`.

Also save related:
- knowledge_state if someone learned/saw/heard something;
- relationships if it affects a known character;
- rumors/reputation if public;
- open_threads if the NPC may return.
