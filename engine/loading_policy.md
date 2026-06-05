# Loading Policy

## Minimal context

Do not load the whole repository. Every turn has a limited file set.

Always load:

- `MANCHESS_RULES.md`
- `engine/turn_contract.md`
- `engine/loading_policy.md`
- `engine/current_frame_policy.md`
- `engine/scene_generation_rules.md`
- `engine/pov_rules.md`
- `engine/output_format.md`
- current runtime `current_state.json`
- current runtime `recent_turns.md`
- active calendar from `current_calendar_id`
- current arc from `current_arc_id`
- current location from `current_location_id`
- `characters/characters_index.yaml`
- `world/academy/academy_index.yaml`

Load conditionally:

- current location detail files;
- active character files;
- scheduled delayed character files when their beat is due;
- mentioned character card and knowledge;
- focused relationships;
- focused knowledge;
- relevant open threads;
- relevant shared incidents;
- public lore by topic;
- hidden lore only by scene tag, arc need or explicit engine rule.

## First day loading

For the first event:

Active first-frame characters:

- `char_akira`
- `char_livia`

Delayed candidates:

- `char_kir`
- `char_kiara`

Social-orbit candidates:

- `char_haru`
- `char_raiden`

Do not load social-orbit candidates as full active scene participants until the current beat or visible scene requires them.

## Character file loading

For active characters, load:

- `character_card.yaml`
- `appearance.md`
- `behavior.md`
- `voice.md`
- `knowledge.yaml`
- `links.yaml`

Load only when needed:

- `energy.yaml` for training, checks, combat or visible energy effect;
- `past.md` for past-triggered scenes;
- `habits.md` for close interaction or body-language-heavy scenes;
- `goals.yaml` when deciding character initiative.

## Avoid

- all characters at once;
- all hidden lore at once;
- all past files at once;
- all scene archive files at once;
- random NPC registry as replacement for concrete character cards;
- relationship assumptions without relationship state or character links.
