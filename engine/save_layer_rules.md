# Save Layer Rules

After a meaningful play scene, call `applyTurnResultSimple`.

Preferred body: direct fields.

Allowed fields include:
- scene_id
- scene_text
- technical
- current_state_changes_json
- knowledge_changes_json
- relationship_changes_json
- open_thread_changes_json
- shared_incident_changes_json
- inventory_changes_json
- character_memory_changes_json
- event_seed_changes_json
- event_queue_changes_json
- director_note_changes_json
- gossip_changes_json
- rating_changes_json
- energy_incident_changes_json

Do not wrap the whole payload into `text`.

Server hotfix 3.4.2 tolerates `{"text":"{...}"}` only as fallback, if the string is valid JSON.
If save fails, the scene is not saved and must not be treated as canon.
