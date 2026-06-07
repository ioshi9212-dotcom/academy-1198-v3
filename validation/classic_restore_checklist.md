# Classic Restore Checklist

After deploy:

- /health returns version 3.5.0.
- getSessionTurnContract returns `contract_version: turn_contract_classic_v2`.
- Response has top-level:
  - active_character_ids;
  - nearby_character_ids;
  - focus_character_ids;
  - required_files;
  - output_format_contract;
  - allowed_new_facts_this_turn;
  - forbidden_new_facts_this_turn;
  - required_checks_before_answer;
  - knowledge_table;
  - inventory_contract;
  - canon_locks;
  - day_contract;
  - relationship_focus;
  - character_runtime_focus.
- scene_contract exists only as backward compatibility note and is not primary.
- No ResponseTooLargeError.
- First scene uses bold speaker names and italic descriptions.
- Akira v2 speech options are not neutral.
- Livia does not sound like a guide.
- 15 Aug ordinary registration does not auto-reveal Akira energy.
- 31 Aug does not publicly classify student energy types.
