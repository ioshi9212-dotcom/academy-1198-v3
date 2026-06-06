# Full Fix Checklist

After deploy:

- health returns version 3.4.2
- createSession without session_id returns random session_id
- createSession with session_id "default" returns random session_id and reserved_session_id_replaced=true
- /sessions/default/turn-contract returns 400
- new random session getSessionTurnContract returns scene_contract_v4_compact_runtime_summaries
- character_slice contains runtime_summary
- applyTurnResultSimple works with normal fields
- applyTurnResultSimple fallback works with {"text": "{...valid json...}"}
