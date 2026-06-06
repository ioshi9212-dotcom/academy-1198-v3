# Как загрузить Scene Assembly Gate в GitHub

Этот пакет не требует терминала.

## Что загрузить

Загрузи файлы в репозиторий с сохранением путей:

```text
engine/scene_assembly_gate.md
validation/scene_assembly_checklist.md
gpt/custom_gpt_instructions_SCENE_GATE_PATCH.md
```

## Важно

Файл `gpt/custom_gpt_instructions_SCENE_GATE_PATCH.md` сам по себе не поменяет Custom GPT.

Его нужно открыть, скопировать блок и вставить в Custom GPT Instructions.

## Что это чинит

- GPT больше не должен писать сцену, если не видит минимальный пакет сцены.
- GPT не должен писать "контракт слишком большой" пользователю.
- GPT не должен восстанавливать формат вручную.
- GPT не должен писать сцену из памяти чата.
- GPT должен сначала собрать шапку/формат/персонажей/память/отношения/знания, потом сцену.
- GPT не должен обнулять давление сцены после аккуратного действия игрока.

## Что ещё желательно

Добавить `engine/scene_assembly_gate.md` в `CORE_REQUIRED_FILES` в `app/main.py`, если ты используешь его как runtime-файл проекта.

Но даже без этого главный блок нужно вставить именно в Custom GPT Instructions.
