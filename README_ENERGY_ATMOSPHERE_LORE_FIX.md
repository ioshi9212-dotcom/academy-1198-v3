# Academy 1198 v3 — Energy Atmosphere Lore Fix

## Что чинит

Академия перестаёт ощущаться обычной школой.

Теперь в scene_contract добавляется:

```text
energy_atmosphere_slice
```

Он напоминает GPT, что Академия — место для носителей энергии.

## Что добавлено

```text
engine/energy_atmosphere_rules.md
runtime/academy/energy_atmosphere.yaml
world/energy/energy_index.yaml
world/energy/general_energy_rules.md
world/energy/classes_and_levels.md
world/energy/restrictions.md
```

## Что изменено

```text
app/main.py
gpt/custom_gpt_instructions_ENERGY_ATMOSPHERE_COMPACT.md
```

## После загрузки

1. Залить файлы в GitHub с сохранением папок.
2. Дождаться Railway Success.
3. Обновить Actions schema:
   https://web-production-cd472.up.railway.app/openapi-actions.json
4. Заменить Custom GPT Instructions на:
   `gpt/custom_gpt_instructions_ENERGY_ATMOSPHERE_COMPACT.md`

## Ожидаемый результат

В обычных сценах Академии появятся малые фоновые проявления энергии:
- кто-то греет стакан;
- холод просачивается от раздражения;
- браслет мигает;
- пол отдаёт резонансом;
- металл щёлкает;
- сотрудник гасит демонстрацию.

Без превращения каждой сцены в фейерверк.
