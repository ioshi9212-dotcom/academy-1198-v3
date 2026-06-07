# Classic Scene Contract Bridge Lock

The project uses `turn_contract_classic_v2` as the main play contract.

However, some GPT/Action layers may still check for a usable `scene_contract` before allowing a play scene.

If `scene_contract.version` is `scene_contract_classic_bridge_v1`, it is usable.

Do not stop with old text:
`Не удалось собрать scene assembly packet через Action...`

Use only the current failure line if the Action itself fails:
`Не удалось собрать turn-contract через Action. Без него я не продолжаю игровую сцену.`

Primary play sources remain:
- top-level `turn_contract_classic_v2`;
- required_files;
- output_format_contract;
- character_runtime_focus;
- relationship_focus;
- knowledge_table;
- day_contract;
- canon_locks.
