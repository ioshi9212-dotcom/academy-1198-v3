# Academy 1198 v3 — готовые файлы для загрузки в GitHub

Это пакет без скриптов. Его можно просто загрузить в GitHub с сохранением папок.

## Как закинуть

1. Открой репозиторий `academy-1198-v3` на GitHub.
2. Нажми `Add file` → `Upload files`.
3. Перетащи содержимое этой папки/ZIP так, чтобы пути сохранились:
   - `app/main.py`
   - `gpt/custom_gpt_instructions.md`
   - `engine/...`
   - `state_templates/...`
   - `relationships/shared_incidents/...`
4. Подтверди commit.
5. Дождись redeploy Railway.
6. В Custom GPT обнови Actions schema из `/openapi-actions.json`.

## Что изменено

- `app/main.py` теперь отдаёт в `scene_contract`:
  - `character_slice`
  - `character_memory_slice`
  - `npc_autonomy_contract`
  - `relationship_behavior_contract`
  - `knowledge_write_contract`
  - `memory_write_contract`
- Active/full персонажи получают behavior/voice прямо в обычном игровом ходе.
- Личная память персонажей читается обратно в следующую сцену.
- Отношения влияют на поведение через levels + `behavior_next`.
- Важные фразы/события сохраняются по уровням важности, а не всё подряд.
- Кир и другие delayed-входы не появляются раньше trigger/story_flag.

## Важно

После замены `app/main.py` старые runtime-сессии могут не иметь новых стартовых relationships/knowledge. Для чистого теста создай новую session.
