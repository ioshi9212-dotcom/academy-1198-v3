# Memory Schema

Runtime memory has three layers.

## 1. Shared incidents

File:

```text
/data/sessions/{session_id}/state/shared_incidents.json
```

Purpose:

Store objective scene events once.

Example:

```json
{
  "incident_1198_08_15_first_access_check": {
    "date": "1198-08-15",
    "day_id": "academy_day_001",
    "location_id": "loc_academy_main",
    "participants": ["char_akira", "char_livia"],
    "witnesses": [],
    "visible_facts": [
      "Akira and Livia entered the Academy flow together.",
      "The entry check showed that access rules are real and immediate."
    ],
    "spoken_lines": [],
    "knowledge_updates": [],
    "relationship_effects": [],
    "status": "active_reference"
  }
}
```

## 2. Relationships

File:

```text
/data/sessions/{session_id}/state/relationships.json
```

Purpose:

Store relationship pair state.

Relationships are not only romance. They include trust, tension, irritation, respect, curiosity, rivalry, debt and unresolved hooks.

Example:

```json
{
  "char_akira__char_livia": {
    "characters": ["char_akira", "char_livia"],
    "status": "close_school_friendship",
    "trust": 70,
    "tension": 10,
    "respect": 45,
    "curiosity": 10,
    "jealousy": 0,
    "shared_incidents": [],
    "open_threads": [],
    "last_interaction": null,
    "behavior_next": "Livia may tease Akira and stay close, but she does not speak for her."
  }
}
```

## 3. Character memory

Folder:

```text
/data/sessions/{session_id}/state/character_memory/
```

Purpose:

Store what each character personally saw, heard, believes or misunderstands.

Example:

```json
{
  "character_id": "char_livia",
  "seen_events": [],
  "heard_events": [],
  "beliefs": [
    {
      "fact_id": "akira_dislikes_control",
      "text": "Akira reacts badly to unnecessary control.",
      "certainty": "high",
      "source": "old friendship"
    }
  ],
  "wrong_beliefs": [],
  "relationships_from_this_character": {
    "char_akira": {
      "trust": 75,
      "tension": 10,
      "private_status": "close friend, difficult but familiar",
      "behavior_next": "Tease, notice, sometimes pull socially, but never decide for Akira."
    }
  }
}
```

## Knowledge rule

A character can only act on:

- what they saw;
- what they heard;
- what they were told;
- what their files allow;
- what they can reasonably infer from visible behavior.

A character cannot act on hidden lore unless the scene gave them a source.
