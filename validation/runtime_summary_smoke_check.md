# Runtime Summary Smoke Check

After deploy, start a new session and call getSessionTurnContract with:

```json
{
  "user_input": "начнем акира версия 2",
  "mode": "play",
  "include_file_contents": false
}
```

Expected in response:

- `success: true`
- `scene_contract.version: scene_contract_v4_compact_runtime_summaries`
- `scene_contract.character_slice.char_akira.runtime_summary`
- `scene_contract.character_slice.char_livia.runtime_summary`
- `scene_contract.scene_assembly_gate`
- no full 6000-char behavior blocks
- no Action size failure
