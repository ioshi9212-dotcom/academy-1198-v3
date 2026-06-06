# Source Priority

When sources conflict, use this single order everywhere in the project:

1. Latest explicit user correction in the current chat.
2. Runtime session state from the active session.
3. `recent_turns.md`, `scene_history.jsonl`, current compacted memory.
4. Current `academy-1198-v3` repository files.
5. Current calendar day and current arc.
6. Active/nearby character files loaded for the scene.
7. Character knowledge, character memory, relationships and shared incidents.
8. Current location files.
9. Old `academy-1198` canon as reference only, adapted to v3 when it does not conflict.
10. `akira-academy-prequel` as style, roster-rotation and academic-social-ecosystem reference only.
11. Public lore.
12. Hidden lore as causal layer only; never as visible NPC knowledge unless a loaded source says the NPC knows it.

## Conflict rule

If a lower-priority source conflicts with a higher-priority source, ignore the lower-priority source for this turn.

If the conflict blocks the scene and cannot be resolved safely, stop and report the conflict instead of guessing.

## NPC knowledge rule

A character can only act from:

- what is visible in the current scene;
- their loaded character files;
- their focused runtime knowledge/memory;
- focused relationship/shared-incident slices;
- facts personally witnessed, heard or learned.

A character must not act from:

- full repository knowledge;
- hidden lore not known to them;
- future plot knowledge;
- another character's private memory;
- old canon that conflicts with current v3 state.
