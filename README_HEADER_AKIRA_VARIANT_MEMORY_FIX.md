# Academy 1198 v3 — Header + Akira Variant + Memory Quality Fix

## Что чинит

1. Шапка:
   - `🫀 Состояние Акиры` больше не тащит одежду/волосы.
   - `🎒 При себе / рядом` показывает коротко: толстовка, джинсы, сумка с одеждой, документы, телефон, волосы распущены, Ливия.
   - "сухая одежда / сухие волосы" не пишется, если это не важно сцене.

2. Акира:
   - общая карточка теперь не задаёт улыбку/выражение лица;
   - выражение, улыбка, тон и поведение идут только из выбранной runtime-версии;
   - добавлены отдельные runtime-файлы:
     - `runtime/characters/akira_v1.yaml`
     - `runtime/characters/akira_v2.yaml`
   - если игрок пишет "Акира версия 2 / v2 / ядовитая", сервер фиксирует `version_2_poisonous`.

3. Мысли/реплики:
   - добавлены правила, что мысли Акиры должны быть короткие, настоящие, практичные и в выбранной версии;
   - для v2 — ядовитая, ленивая оценка риска/людей, не авторская философия.

4. Всё предыдущее сохранено:
   - compact scene_contract;
   - session_id защита от default;
   - save layer fix для applyTurnResultSimple.

## Что загрузить

Загрузи всё в GitHub с сохранением папок. Главное:

```text
app/main.py
state_templates/current_state.json
runtime/characters/characters_runtime_index.yaml
runtime/characters/akira_v1.yaml
runtime/characters/akira_v2.yaml
characters/akira/appearance.md
engine/header_quality_rules.md
engine/akira_variant_rules.md
gpt/custom_gpt_instructions_HEADER_VARIANT_COMPACT.md
```

Также в ZIP есть остальные runtime summaries, чтобы не потерять их.

## После загрузки

1. Railway Deployments → дождаться Success.
2. Проверить:
   `https://web-production-cd472.up.railway.app/health`
3. Обновить Actions schema:
   `https://web-production-cd472.up.railway.app/openapi-actions.json`
4. В Custom GPT Instructions заменить текст на:
   `gpt/custom_gpt_instructions_HEADER_VARIANT_COMPACT.md`
