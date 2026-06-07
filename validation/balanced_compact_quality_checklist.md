# Balanced Compact Quality Checklist

After deploy:

- /health version is 3.4.9.
- getSessionTurnContract returns success on long session.
- scene_contract.version is scene_contract_v5_balanced_compact.
- current_state_summary shows active/nearby/mentioned/scheduled/delayed ids.
- character_load_plan has focus_reference_character_ids when relevant.
- character_slice includes runtime_summary for active + focus references.
- scene_quality/progress/prose contracts are not one-line-only.
- No ResponseTooLargeError.
- Scene is no longer short/generic.
