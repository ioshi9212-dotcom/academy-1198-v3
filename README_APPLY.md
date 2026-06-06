# academy-1198-v3 fixes package

Пакет исправлений для `ioshi9212-dotcom/academy-1198-v3`.

## Что внутри

### 1. Runtime memory fix

Главное исправление — `app/main.py`:

- `relationships.json` читается из `relationships`;
- `knowledge_state.json` читается из `character_knowledge`;
- `open_threads.json` читается из `threads`;
- `shared_incidents.json` читается из `incidents`;
- `event_seeds`, `event_queue`, `gossip_state`, `energy_incidents` читаются из `items`, но поддерживают старый top-level формат;
- новые state-patches автоматически складываются в правильные контейнеры;
- `applyTurnResultSimple` больше не съедает битый JSON молча, а отдаёт `400 Bad Request` с указанием поля.

### 2. Source priority fix

Выровнены:

- `engine/source_priority.md`
- `engine/current_frame_policy.md`
- `engine/loading_policy.md`
- `gpt/engine_prompt.md`

Теперь порядок источников один, без противоречий.

### 3. Raiden fill

Заполнены файлы:

- `characters/raiden/character_card.yaml`
- `characters/raiden/appearance.md`
- `characters/raiden/behavior.md`
- `characters/raiden/voice.md`
- `characters/raiden/knowledge.yaml`
- `characters/raiden/links.yaml`
- `characters/raiden/energy.yaml`
- `characters/raiden/habits.md`
- `characters/raiden/goals.yaml`
- `characters/raiden/past.md`

### 4. Event templates format

Приведены к единому контейнерному формату:

- `state_templates/event_seeds.json`
- `state_templates/event_queue.json`

## Как применить

### Вариант А — вручную через GitHub

1. Распакуй ZIP.
2. Загрузи/замени все файлы из папок `engine`, `gpt`, `characters`, `state_templates`, `scripts`, `PATCHES`, `docs` в репозиторий.
3. Для `app/main.py` применить надо не обычной загрузкой, а патчем:
   - либо через `PATCHES/app_main_runtime_slices_and_json_validation.patch`;
   - либо через скрипт `scripts/apply_1198_v3_fixes.py`.

### Вариант Б — локально через Python

Из корня репозитория:

```bash
python scripts/apply_1198_v3_fixes.py
```

После этого:

```bash
python -m py_compile app/main.py
```

Потом commit/push.

## Важно

ZIP не удаляет старые `PATCH_*` файлы в корне репозитория. Их лучше отдельно перенести в `docs/patch_history/` или удалить после проверки.
