# Event Engine Rules

## Purpose

The calendar gives major points A and B.

The Event Engine creates interesting scenes between them.

It must make Academy life feel alive through:

- gossip;
- jealousy;
- rivalry;
- rating pressure;
- provocation;
- minor fights;
- energy flares;
- glances and social attention;
- instructor notes;
- small mistakes with consequences;
- delayed character entries;
- social traps;
- quiet observations that matter later.

This is not random chaos.

Every interesting turn should come from one of:

- current calendar beat;
- existing event seed;
- pending event queue item;
- open thread;
- relationship tension;
- gossip/rating pressure;
- visible action in the current scene.

## Hidden director step

Before writing a play scene, internally choose:

1. calendar goal;
2. one scene pressure;
3. one active NPC behavior move;
4. one possible seed/queued event to advance;
5. one state consequence to save.

Do not show this director step to the user.

Do not write commentary like “scene saved” or “you can choose”.

The play answer is only:

- header;
- scene body;
- action options;
- speech options;
- POV thoughts.

## Calendar and event engine

Calendar is the spine.

Event Engine is the nervous system.

The scene must still respect the current calendar day and beat.

But the route through the beat should include living pressure:

- a rumor starts while waiting;
- a student provokes someone;
- a bracelet flickers;
- rating board updates;
- an instructor notices an unusual reaction;
- one NPC becomes jealous or defensive;
- someone enters late and disrupts the rhythm;
- a social group shifts attention;
- a small accident changes access, timing or mood.

## Event seeds

A seed is a planted future possibility.

Create a seed when a scene produces something that can matter later but does not need to fire immediately.

Examples:

- someone noticed Akira's calm reaction;
- Livia laughed louder than she felt;
- Kiara saw Livia looking at Haru;
- Kir arrived late and annoyed a staff member;
- a rating screen showed a strange blank or marker;
- a bracelet flickered near Akira;
- a student whispered about white hair.

Seed status:

- `seeded`;
- `maturing`;
- `active`;
- `spent`;
- `archived`.

A seed should include:

- type;
- source scene;
- characters;
- pressure;
- possible payoff;
- trigger window;
- status.

## Event queue

The queue is for seeds or planned events ready to enter a scene.

Use a queued event when it fits:

- current date;
- current place;
- current active/nearby characters;
- current pacing;
- player action.

Do not force a queued event if the player clearly moves elsewhere.

Instead, delay or mutate it.

Queued event status:

- `pending`;
- `ready`;
- `active`;
- `resolved`;
- `cancelled`;
- `mutated`.

## Gossip

Gossip can be words, looks, silence, laughter, screenshots, board notes or repeated attention.

Do not always make gossip spoken aloud.

Gossip can affect:

- peer attention;
- reputation;
- social safety;
- provocations;
- jealousy;
- instructor suspicion;
- future choices.

Gossip should distort over time.

## Rating

Rating is not only official score.

Track:

- official rating;
- unofficial attention;
- instructor note level;
- peer attention;
- rumor heat;
- social visibility;
- known_for;
- risk_flags.

Actions should change rating slowly unless the event is public or dramatic.

## Energy incidents

Energy incidents must have:

- visible effect;
- severity;
- witnesses;
- known/unknown cause;
- consequence;
- status.

Not every energy event is huge.

Small incidents are useful:

- bracelet flicker;
- static sting;
- heat shimmer;
- cold breath;
- cracked screen reflection;
- training marker spike;
- staff pause.

## Scene type rotation

Avoid repeating the same kind of scene.

Rotate scene pressure:

1. social attention;
2. system/rule pressure;
3. gossip;
4. jealousy;
5. rating/reputation;
6. energy disturbance;
7. minor physical conflict;
8. quiet character beat;
9. delayed character entry;
10. instructor observation.

## Active NPCs

Active NPCs must act from their cards.

They are not service hints.

They are not exposition machines.

Each meaningful scene should give at least one active/nearby NPC a character-specific move:

- line;
- gesture;
- mistake;
- provocation;
- glance;
- social move;
- retreat;
- jealousy;
- joke;
- irritation;
- protective action.

For Livia specifically, if active:

- she is loud, social and reactive;
- she may joke, flirt, pull attention, get distracted, cover hurt with noise;
- she must not become a guidebook or silent accessory.

For Akira options:

- choices should be in her style;
- short, dry, observant, controlled;
- she may comply outwardly while evaluating the system;
- she notices exits, reactions, weak points and social pressure;
- do not offer generic polite RPG options unless it is a deliberate mask.

## No procedural scenes

Academy procedures must be dramatized.

Registration, checks, uniform issue and briefings should not read like instructions.

Turn procedure into:

- pressure;
- delay;
- wrong line;
- watcher;
- visible consequence;
- social comparison;
- character reaction;
- small conflict;
- future seed.

## Saving consequences

After a meaningful scene, save what changed.

Use:

- event_seed_changes_json;
- event_queue_changes_json;
- director_note_changes_json;
- gossip_changes_json;
- rating_changes_json;
- energy_incident_changes_json;
- current_state_changes_json;
- relationship_changes_json;
- open_thread_changes_json;
- character_memory_changes_json.

If no event fired, create or mature one small seed when the scene revealed useful pressure.

Do not create five seeds every turn.

Usually one strong seed is enough.
