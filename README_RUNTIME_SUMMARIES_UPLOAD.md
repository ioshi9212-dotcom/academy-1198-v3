# Academy 1198 v3 — Runtime Summaries Hotfix

Этот пакет делает `scene_contract` компактным.

## Что внутри

```text
app/main.py
runtime/characters/characters_runtime_index.yaml
runtime/characters/akira.yaml
runtime/characters/livia.yaml
runtime/characters/kir.yaml
runtime/characters/kiara.yaml
runtime/characters/haru.yaml
runtime/characters/raiden.yaml
engine/runtime_character_slice_rules.md
gpt/custom_gpt_instructions_RUNTIME_SUMMARY_PATCH.md
```

## Что заменить в GitHub

Загрузи файлы в репозиторий `academy-1198-v3` с сохранением папок.

Главный файл для замены:

```text
app/main.py
```

## Что изменилось

`scene_contract` больше не отдаёт полные `behavior.md` и `voice.md` каждый ход.

Вместо этого он отдаёт компактные файлы:

```text
runtime/characters/{character}.yaml
```

Так сохраняется характер персонажей, но Action не падает от слишком большого ответа.

## После загрузки

1. Дождись Railway deploy Success.
2. Проверь:
   `https://web-production-cd472.up.railway.app/health`
3. Обнови schema в Custom GPT:
   `https://web-production-cd472.up.railway.app/openapi-actions.json`
4. В Custom GPT Instructions добавь текст из:
   `gpt/custom_gpt_instructions_RUNTIME_SUMMARY_PATCH.md`

## Что ожидать

`getSessionTurnContract` должен начать проходить без ошибки размера.

Если он всё равно падает — значит нужно ещё сильнее резать `calendar_slice`/`event_engine_slice`, но сначала этот hotfix должен убрать главный перегруз: character behavior/voice.
