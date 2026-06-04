# Turn Contract

Before every play-scene answer, the engine must:

1. Read current runtime session state.
2. Read recent_turns.
3. Check current year, date, day_id, time, location and arc.
4. Check active calendar by current_calendar_id.
5. Load active characters by ID only.
6. Load mentioned characters only if the user input or active state requires them.
7. Load focused knowledge and focused relationships.
8. Load shared incidents only when linked to active characters or open threads.
9. Load hidden lore only as a hidden causal layer, not NPC knowledge.
10. Write scene through Akira-visible POV.
11. Stop at a meaningful intervention point.
12. Provide action options, line options and true thoughts.
13. Persist meaningful state changes through the API.
