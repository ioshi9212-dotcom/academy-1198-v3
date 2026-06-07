# Generic Instructions Update

This update removes project-specific character/day rules from Custom GPT Instructions.

Custom GPT Instructions now describe only engine behavior:
- how to use API/Actions;
- how to read turn_contract_classic_v2;
- how to use required_files;
- how to write scenes;
- how to validate voice;
- how to handle knowledge, inventory, calendar, memory/save;
- how to avoid empty scenes and micro-choices.

Specific facts about characters, days, calendar events, energy privacy, and hidden lore must live in:
- runtime character files;
- calendar files;
- canon locks;
- state files;
- required_files;
- turn_contract fields.

Use:
`gpt/custom_gpt_instructions_CLASSIC_RESTORE.md`
or same copy:
`gpt/custom_gpt_instructions_ENGINE_ONLY.md`
