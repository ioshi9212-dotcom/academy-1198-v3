# GitHub Actions pre-merge runtime test

Залей эти файлы в репозиторий `academy-1198-v3` с сохранением папок:

```text
.github/workflows/premerge-runtime-check.yml
scripts/local_smoke_test.py
```

После этого GitHub Actions будет запускать проверку:

- при Pull Request в `main`;
- при push в `main`;
- вручную через вкладку **Actions → Pre-merge Runtime Check → Run workflow**.

## Что проверяет тест

Тест не играет художественную сцену. Он проверяет runtime-контур:

1. Создаётся новая session.
2. `get_turn_contract` отдаёт старт 1198-08-15, Академию, Акиру и Ливию.
3. `scene_contract` содержит обязательные слои:
   - `character_slice`;
   - `character_memory_slice`;
   - `npc_autonomy_contract`;
   - `relationship_behavior_contract`;
   - `knowledge_write_contract`;
   - `memory_write_contract`.
4. У Акиры и Ливии реально загружены `behavior` и `voice`.
5. Стартовая связь Акира/Ливия есть в `relationships.json`.
6. Знания Ливии есть в `knowledge_state.json`.
7. `applyTurnResultSimple` сохраняет:
   - важную фразу Акиры;
   - shared incident;
   - relationship update;
   - character memory.
8. Следующий `get_turn_contract` читает эту память обратно.
9. Битый JSON не проглатывается молча, а валится ошибкой 400.

Если тест красный — merge/deploy лучше не делать.
