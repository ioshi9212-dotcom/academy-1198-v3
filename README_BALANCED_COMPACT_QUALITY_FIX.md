# Academy 1198 v3 — Balanced Compact Quality Fix

## Что чинит

После ultra compact сцены стали слишком короткими и тупыми.

Причина:
- scene_quality/progress/prose contracts были слишком сжаты;
- runtime_summary слишком обрезались;
- Кир/Киара шли как reference/delayed без runtime_summary;
- event_engine/energy/knowledge были урезаны слишком сильно.

## Что изменено

Теперь play-mode возвращает:

```text
scene_contract_v5_balanced_compact
```

Он всё ещё защищает от ResponseTooLargeError, но возвращает больше полезного для качества.

## Главное

- Active summaries стали длиннее.
- До 2 reference/delayed персонажей получают focus runtime summaries.
- scene_quality/progress/prose contracts стали богаче.
- event_engine/energy/knowledge немного расширены.
- current_state_summary явно показывает active/nearby/mentioned/scheduled/delayed.
- Akira v2 drift fix сохранён.

## Что загрузить

Загрузи всё в GitHub с сохранением папок. Главное:

```text
app/main.py
engine/balanced_compact_contract_rules.md
gpt/custom_gpt_instructions_BALANCED_COMPACT.md
validation/balanced_compact_quality_checklist.md
```

## После загрузки

1. Commit directly to main.
2. Дождаться Railway Success.
3. Проверить:
   https://web-production-cd472.up.railway.app/health
4. Обновить Actions schema:
   https://web-production-cd472.up.railway.app/openapi-actions.json
5. Заменить Custom GPT Instructions на:
   `gpt/custom_gpt_instructions_BALANCED_COMPACT.md`
