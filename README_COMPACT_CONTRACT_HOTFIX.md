# Compact Turn Contract Hotfix

Проблема: `getSessionTurnContract` падал из-за слишком большого ответа.

Что изменено в `app/main.py`:

- `character_slice` теперь компактный: behavior/voice остаются, но как короткие срезы.
- `character_memory_slice` больше не отдаёт всю память персонажа, только последние важные элементы.
- `calendar_slice`, `arc_slice`, `location_slice` уменьшены.
- `event_engine_slice` отдаёт меньше items.
- Версия API в root/health оставлена совместимой, endpoints не менялись.

Как ставить:

1. В GitHub замени файл `app/main.py` на этот.
2. Дождись Railway deploy.
3. После deploy обнови Actions schema:
   `https://web-production-cd472.up.railway.app/openapi-actions.json`
4. Начни новую сессию.

Ожидаемый результат:

- Action `getSessionTurnContract` должен перестать падать от размера.
- GPT сможет собрать scene assembly packet.
- Если всё ещё падает, значит нужно ещё сильнее резать `character_slice` или top-level `current_state`.
