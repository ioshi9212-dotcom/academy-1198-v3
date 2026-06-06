# Scene Assembly Checklist

Use before every play response.

## Required before scene

- [ ] current_state loaded
- [ ] scene_contract loaded
- [ ] current_frame present
- [ ] header_values present
- [ ] header_contract present
- [ ] response_format_contract present
- [ ] scene_density_contract present
- [ ] full_character_ids present
- [ ] character_slice present
- [ ] behavior/voice present for every full character
- [ ] relationship_slice present
- [ ] knowledge_slice present
- [ ] character_memory_slice present
- [ ] npc_autonomy_contract present
- [ ] relationship_behavior_contract present
- [ ] memory_write_contract present
- [ ] event_engine_slice present

If any required item is missing: stop. Do not write scene.

## Required before sending

- [ ] no technical text in response
- [ ] emoji header shell used
- [ ] action options present
- [ ] speech options present
- [ ] thoughts present
- [ ] active NPCs behave from character
- [ ] world does not obey player intent automatically
- [ ] scene pressure remains alive
- [ ] at least one trace/consequence exists
