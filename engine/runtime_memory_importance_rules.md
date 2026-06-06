# Runtime Memory Importance Rules

## Purpose

This file defines what must be read now, what may influence the scene, and what must be saved after a meaningful turn.

The engine must not save everything. It must save what has future narrative value.

## Reading priority per turn

### CRITICAL

Must be read and used if present:

- current_state;
- current_frame;
- current calendar day block;
- current arc;
- current location;
- POV character full slice;
- active and nearby character slices;
- relationship_slice between present characters;
- knowledge_slice for present characters;
- character_memory_slice for present characters;
- open threads blocking current scene;
- shared incidents involving present characters;
- event queue item marked ready/active and matching scene;
- body/clothing/item continuity affecting current scene.

### FOCUSED

Use if it creates scene pressure:

- scheduled/delayed character whose trigger is due;
- event seeds with matching date/location/characters;
- gossip/rating/energy incidents near current scene;
- relationship memory with a direct behavioral effect;
- character goals/details when they drive initiative.

### REFERENCE

Do not use unless explicitly needed:

- hidden lore;
- whole calendar;
- all relationships;
- all character files;
- all rumors;
- future 1206 facts;
- distant characters not present.

## What counts as a meaningful event

Save an event if it has future value:

- public conflict;
- private conflict that changes relationship;
- important line/warning/promise/refusal;
- someone learns a name or fact;
- someone forms suspicion or wrong belief;
- rule consequence;
- access/rating/reputation change;
- injury/body/clothing/item change;
- energy incident;
- witnessable social moment;
- open thread or future hook;
- character boundary is crossed or defended.

Do not save routine alone.

## Important spoken lines

Save a spoken line only if it changes relationship, becomes a future hook, is heard by witnesses, could become a rumor, reveals a boundary, creates a promise/debt/refusal/threat, shows character unusually strongly, changes someone’s belief, humiliates, protects, warns or challenges someone.

Preferred structure:

```json
{
  "speaker": "char_akira",
  "text": "exact or close paraphrase",
  "heard_by": ["char_livia"],
  "importance": "high",
  "effect": "raised tension / created rumor / changed belief",
  "tags": ["boundary", "provocation"]
}
```

## Knowledge write schema

Use `knowledge_changes_json` for character knowledge.

```json
{
  "character_knowledge": {
    "char_livia": {
      "facts": {
        "fact_id": {
          "text": "",
          "certainty": "low|medium|high|confirmed",
          "source": "seen_directly|heard_directly|told_by_character|inferred_from_behavior|rumor",
          "scene_id": "",
          "date": "",
          "about": ["char_akira"]
        }
      },
      "suspicions": {},
      "wrong_beliefs": {}
    }
  },
  "evidence_log": [
    {
      "fact_id": "",
      "source_scene_id": "",
      "who_knows": ["char_livia"],
      "evidence": ""
    }
  ],
  "speaker_labels": {}
}
```

## Relationship write schema

Use `relationship_changes_json`.

```json
{
  "relationships": {
    "char_akira__char_livia": {
      "characters": ["char_akira", "char_livia"],
      "status": "close_school_friendship",
      "levels": {
        "trust": 75,
        "tension": 12,
        "respect": 50,
        "curiosity": 10,
        "jealousy": 0,
        "resentment": 0,
        "affection": 35
      },
      "memory": [
        {
          "scene_id": "",
          "summary": "",
          "evidence": "",
          "importance": "medium|high|critical"
        }
      ],
      "open_threads": [],
      "shared_incidents": [],
      "behavior_next": "",
      "last_interaction": {
        "scene_id": "",
        "date": "",
        "summary": ""
      }
    }
  }
}
```

Relationship changes must have evidence.

## Character memory write schema

Use `character_memory_changes_json`.

```json
{
  "char_livia": {
    "seen_events": [],
    "heard_events": [],
    "remembered_lines": [],
    "beliefs": [],
    "wrong_beliefs": [],
    "relationship_notes": {
      "char_akira": []
    },
    "relationships_from_this_character": {
      "char_akira": {
        "trust": 75,
        "tension": 12,
        "private_status": "",
        "behavior_next": ""
      }
    },
    "scene_behavior_overrides": []
  }
}
```

## Behavior use rule

Before writing an NPC reaction, check:

1. character_slice behavior/voice;
2. knowledge_slice;
3. character_memory_slice;
4. relationship_slice;
5. relationship_behavior_contract;
6. active scene pressure.

The NPC must not behave from author knowledge alone.

## Relationship levels to behavior

- trust high: closer distance, less defensive, may warn or help, but not obey automatically;
- tension high: sharper tone, avoidance, challenge, clipped replies;
- respect high: takes seriously even when disagreeing;
- curiosity high: watches, tests, asks, follows details;
- jealousy high: compares, competes for attention, masks hurt;
- resentment high: remembers offense, coldness, refusal, delayed payback;
- affection high: small softness/protection, but still boundaries and goals.

## After-scene minimum

For each meaningful scene, save at least one of:

- shared incident;
- relationship change;
- knowledge change;
- character memory update;
- open thread;
- event queue/seed update;
- current_state change.

If none are worth saving, the scene was probably not meaningful enough.
