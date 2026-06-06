# Academy 1198 v3 — Scene Progress + Factual Prose Fix

## Что чинит

1. Не зависать на микрошаге.
2. Не давать бессмысленные выборы типа:
   - нажать кнопку автомата;
   - ждать инструкций;
   - посмотреть на панель;
   - взять карточку.
3. Меньше художественности.
4. Больше чётких фактов, физических эффектов и последствий.

## Пример стиля

Плохо:
`Белые волосы отражают холодный свет панели, контрастируя с серостью коридора.`

Хорошо:
`Белые волосы заметны в холодном свете панели.`

Плохо:
`Воздух будто задержал дыхание.`

Хорошо:
`Шум очереди стал тише на секунду.`

## Что изменено

```text
app/main.py
engine/prose_style_rules.md
engine/scene_progress_rules.md
gpt/custom_gpt_instructions_SCENE_PROGRESS_FACTUAL_PROSE_COMPACT.md
validation/prose_and_progress_checklist.md
```

Сохранены предыдущие фиксы:
- energy atmosphere;
- no-stub scene quality;
- Akira v1/v2;
- header split;
- session guard;
- save layer.

## После загрузки

1. Залить файлы в GitHub с сохранением папок.
2. Дождаться Railway Success.
3. Обновить Actions schema:
   https://web-production-cd472.up.railway.app/openapi-actions.json
4. Заменить Custom GPT Instructions на:
   `gpt/custom_gpt_instructions_SCENE_PROGRESS_FACTUAL_PROSE_COMPACT.md`
