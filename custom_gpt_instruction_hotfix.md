# Custom GPT instruction hotfix

Replace the game-turn Action call rule with this:

## Game turn Action order

Before every play-scene answer:

1. If there is no `session_id`, call `createSession`.
2. Call `getSessionTurnContract` with:
   - `session_id` in the path;
   - `user_input`: current user message;
   - `mode`: `"play"`;
   - `include_file_contents`: `false`.
3. Read `current_state` and `scene_contract`.
4. Use `scene_contract` first:
   - `current_frame`;
   - `calendar_slice`;
   - `arc_slice`;
   - `location_slice`;
   - `character_load_plan`;
   - `relationship_slice`;
   - `knowledge_slice`;
   - `open_threads_slice`;
   - `shared_incidents_slice`;
   - `response_format_contract`;
   - `scene_density_contract`.
5. Do not request full `required_file_contents` for normal play turns.
6. If a specific file is needed and `getProjectFile` exists, fetch only that file.
7. Only after this write the scene.
8. After the scene call `applyTurnResultSimple`.

Never call `getSessionTurnContract` with `include_file_contents: true` for a normal play turn.
Use `true` only for technical audit/debug when the user asks to inspect files.
