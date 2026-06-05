# Turn Contract

Before every play-scene answer, the engine must:

1. Read the current runtime session state.
2. Read `recent_turns`.
3. Check current year, date, day_id, time, location, arc and calendar.
4. Check active calendar by `current_calendar_id`.
5. Check active arc by `current_arc_id`.
6. Check current location by `current_location_id`.
7. Load the Academy index and the Academy files needed for the current scene.
8. Load active characters by ID only.
9. Load scheduled delayed characters only if their beat is due.
10. Load mentioned characters only if the user input or active state requires them.
11. Load focused relationships and focused knowledge.
12. Load open threads connected to active characters, current location or current calendar event.
13. Load shared incidents only when linked to active characters, open threads or current consequences.
14. Treat hidden lore as causal background only, not as NPC knowledge.
15. Write the scene through Akira-visible POV.
16. Stop at a meaningful intervention point.
17. Provide action options, line options and true thoughts.
18. Persist meaningful state changes through the API.

If required files are missing, state what is missing instead of continuing from guesswork.
