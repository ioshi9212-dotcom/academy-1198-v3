# Characters

This folder stores canon character files. Runtime changes, memories, and scene-specific relationship shifts live in Railway Volume, not here.

## Character folder structure

Each important character should have a folder:

```text
characters/<character_id_slug>/
├── character_card.yaml   # machine-readable passport
├── profile.md            # human-readable questionnaire
├── appearance.md         # fixed appearance
├── behavior.md           # behavior rules
├── voice.md              # speech style
├── knowledge.yaml        # canon starting knowledge
├── energy.yaml           # energy type and limits
├── past.md               # past, only if needed
├── habits.md             # small physical/social habits
├── goals.yaml            # current and hidden goals
└── links.yaml            # relationships, incidents, runtime refs
```

## Creation order

1. Copy `character_template/`.
2. Rename folder to a stable slug, for example `raiden/` or `livia/`.
3. Fill `character_card.yaml` first.
4. Fill `profile.md` in normal language.
5. Split details into appearance, behavior, voice, knowledge, energy, past, habits, goals.
6. Register the character in `characters_index.yaml`.
7. Add relationship pairs only if needed.

## Hard rules

- Do not create important NPCs without stable IDs.
- Do not reuse aliases between characters.
- Do not put runtime relationship changes into canon character files.
- Do not put hidden lore into NPC knowledge unless the character starts with that knowledge.
- Do not use a character in scene without checking whether Akira knows their name.
