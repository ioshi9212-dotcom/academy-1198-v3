# app/main.py — что должен сделать авто-патч

`apply_v3_runtime_patch.py` вносит изменения idempotently.

## Добавляет в CORE_REQUIRED_FILES

```python
"engine/npc_autonomy_rules.md",
```

## Добавляет функцию

```python
def build_character_slice(session_id: str, character_ids: list[str]) -> dict[str, Any]:
    ...
```

Она кладёт в `scene_contract` компактные тексты active/full персонажей:

- character_card
- behavior
- voice
- knowledge

## Добавляет функцию

```python
def npc_autonomy_contract() -> dict[str, Any]:
    ...
```

Она прямо объясняет модели, что игрок не управляет NPC.

## В `build_scene_contract()` добавляет

```python
"character_slice": build_character_slice(session_id, selected["full"]),
"npc_autonomy_contract": npc_autonomy_contract(),
```

## В `event_engine_slice.selection_protocol` добавляет

```python
"Do not use locked/pending delayed character entries until their trigger_after or requires_story_flag is satisfied.",
```

## В `checks` ответа turn-contract добавляет

```python
"Use scene_contract.character_slice for full active characters before writing their dialogue.",
"Use npc_autonomy_contract: NPC commands are attempts, not guaranteed outcomes.",
```

## Чуть правит шапку

- `format_weather_human()` делает ветер читаемее.
- `format_pov_state_human()` больше не пишет `без травм` автоматически.
