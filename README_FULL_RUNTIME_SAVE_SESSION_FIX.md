# Academy 1198 v3 — Full Runtime + Save + Session Fix

## Что чинит

1. Compact scene contract:
   - вместо full `behavior.md/voice.md` используются `runtime/characters/*.yaml`.
   - `getSessionTurnContract` не должен падать от размера.

2. Session safety:
   - `default`, `new`, `none`, `null`, `undefined`, `session` запрещены как игровые session_id.
   - `createSession` с `session_id: "default"` создаёт новую random-сессию.

3. Save layer:
   - `applyTurnResultSimple` принимает нормальные поля.
   - дополнительно терпит ошибку GPT, когда весь payload отправлен как `{"text": "{...json...}"}`.
   - если text невалидный/обрезанный — вернёт понятную 400 ошибку.

4. Prompt:
   - готовая короткая Custom GPT instruction до лимита.
   - добавлены session rule и save rule.

## Что загрузить в GitHub

Загрузи всё с сохранением папок. Главное:

```text
app/main.py
runtime/characters/*.yaml
engine/runtime_character_slice_rules.md
engine/save_layer_rules.md
gpt/custom_gpt_instructions_FULL_COMPACT.md
```

## После загрузки

1. Дождаться Railway Deployments → Success.
2. Открыть:
   https://web-production-cd472.up.railway.app/health
3. Обновить Actions schema:
   https://web-production-cd472.up.railway.app/openapi-actions.json
4. В Custom GPT Instructions вставить весь текст из:
   `gpt/custom_gpt_instructions_FULL_COMPACT.md`

## Важно

Старую сессию `default` лучше не считать чистой каноничной сессией. Она могла смешать состояние.

Для чистой проверки начни новый чат и попроси:
`Начнем. Создай новую сессию. Не используй default.`
