from __future__ import annotations

import json
import os
import re
from typing import Any, Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field

from app.core.storage import (
    append_jsonl,
    debug_info,
    ensure_runtime_root,
    ensure_session,
    read_json,
    read_project_or_runtime_file,
    read_state,
    safe_repo_path,
    session_root,
    session_state_root,
    utc_now,
    write_json_atomic,
    write_state,
)

PROJECT_SLUG = os.getenv("PROJECT_SLUG", "academy-1198-v3")
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")
COMPACT_EVERY_TURNS = int(os.getenv("COMPACT_EVERY_TURNS", "15"))
MAX_FILE_CHARS = int(os.getenv("MAX_FILE_CHARS", "18000"))
MAX_SCENE_SLICE_CHARS = int(os.getenv("MAX_SCENE_SLICE_CHARS", "6000"))

app = FastAPI(title=f"{PROJECT_SLUG} GPT Actions API", version="3.2.1")


class CreateSessionRequest(BaseModel):
    session_id: str | None = None
    reset: bool = True


class TurnContractRequest(BaseModel):
    user_input: str = ""
    mode: Literal["play", "technical", "audit", "transfer"] = "play"
    include_file_contents: bool = False


class ApplyTurnResultRequest(BaseModel):
    scene_id: str = "scene"
    scene_text: str = ""
    technical: bool = False
    current_state_changes: dict[str, Any] = Field(default_factory=dict)
    knowledge_changes: dict[str, Any] = Field(default_factory=dict)
    relationship_changes: dict[str, Any] = Field(default_factory=dict)
    open_thread_changes: dict[str, Any] = Field(default_factory=dict)
    shared_incident_changes: dict[str, Any] = Field(default_factory=dict)
    inventory_changes: dict[str, Any] = Field(default_factory=dict)
    character_memory_changes: dict[str, Any] = Field(default_factory=dict)

    event_seed_changes: dict[str, Any] = Field(default_factory=dict)
    event_queue_changes: dict[str, Any] = Field(default_factory=dict)
    director_note_changes: dict[str, Any] = Field(default_factory=dict)
    gossip_changes: dict[str, Any] = Field(default_factory=dict)
    rating_changes: dict[str, Any] = Field(default_factory=dict)
    energy_incident_changes: dict[str, Any] = Field(default_factory=dict)


class ApplyTurnResultSimpleRequest(BaseModel):
    scene_id: str = "scene"
    scene_text: str = ""
    technical: bool = False
    current_state_changes_json: str = "{}"
    knowledge_changes_json: str = "{}"
    relationship_changes_json: str = "{}"
    open_thread_changes_json: str = "{}"
    shared_incident_changes_json: str = "{}"
    inventory_changes_json: str = "{}"
    character_memory_changes_json: str = "{}"

    event_seed_changes_json: str = "{}"
    event_queue_changes_json: str = "{}"
    director_note_changes_json: str = "{}"
    gossip_changes_json: str = "{}"
    rating_changes_json: str = "{}"
    energy_incident_changes_json: str = "{}"


class CompactRequest(BaseModel):
    reason: str = "scheduled_compaction"
    compact_last_turns: int = 15
    recent_turns_md: str | None = None
    state_updates: dict[str, Any] = Field(default_factory=dict)


CORE_REQUIRED_FILES = [
    "engine/novel_director_core.md",
    "engine/output_format.md",
    "engine/scene_generation_rules.md",
    "engine/event_engine_rules.md",
    "engine/pov_rules.md",
    "engine/memory_update_rules.md",
    "story/pacing/no_filler_rules.md",
    "state/current_state.json",
    "state/recent_turns.md",
    "characters/characters_index.yaml",
    "world/locations/locations_index.yaml",
    "knowledge/knowledge_rules.md",
]

TECHNICAL_EXTRA_FILES = [
    "MANCHESS_RULES.md",
    "engine/turn_contract.md",
    "engine/loading_policy.md",
    "engine/source_priority.md",
    "engine/session_policy.md",
    "engine/npc_knowledge_rules.md",
    "engine/anti_hallucination_rules.md",
    "validation/checklist_before_scene.md",
    "validation/calendar_skip_check.md",
    "validation/npc_knowledge_check.md",
    "validation/pov_violation_check.md",
    "relationships/relationships_index.yaml",
    "relationships/pair_schema.yaml",
]

AUDIT_EXTRA_FILES = [
    "validation/checklist_after_scene.md",
    "relationships/shared_incidents/incidents_index.yaml",
    "relationships/shared_incidents/incident_template.yaml",
]


def character_core_files(folder: str) -> list[str]:
    return [
        f"characters/{folder}/character_card.yaml",
        f"characters/{folder}/appearance.md",
        f"characters/{folder}/behavior.md",
        f"characters/{folder}/voice.md",
        f"characters/{folder}/knowledge.yaml",
        f"characters/{folder}/links.yaml",
    ]


def character_light_files(folder: str) -> list[str]:
    return [f"characters/{folder}/character_card.yaml"]


def character_goal_files(folder: str) -> list[str]:
    return [f"characters/{folder}/goals.yaml"]


def character_detail_files(folder: str) -> list[str]:
    return [
        f"characters/{folder}/energy.yaml",
        f"characters/{folder}/habits.md",
        f"characters/{folder}/past.md",
    ]


CHARACTER_FOLDERS: dict[str, str] = {
    "char_akira": "akira",
    "char_livia": "livia",
    "char_kir": "kir",
    "char_kiara": "kiara",
    "char_haru": "haru",
    "char_raiden": "raiden",
    "char_samuel": "samuel",
}

LOCATION_REQUIRED_FILES: dict[str, list[str]] = {
    "loc_academy_main": [
        "world/locations/academy_main/location_card.yaml",
        "world/locations/academy_main/visual_description.md",
    ],
}

MONTHS_RU = {
    1: "января",
    2: "февраля",
    3: "марта",
    4: "апреля",
    5: "мая",
    6: "июня",
    7: "июля",
    8: "августа",
    9: "сентября",
    10: "октября",
    11: "ноября",
    12: "декабря",
}

WEEKDAY_SHORT = {
    "понедельник": "пн",
    "вторник": "вт",
    "среда": "ср",
    "четверг": "чт",
    "пятница": "пт",
    "суббота": "сб",
    "воскресенье": "вс",
}

TIME_OF_DAY_RU = {
    "morning": "Утро",
    "day": "День",
    "afternoon": "День",
    "evening": "Вечер",
    "night": "Ночь",
}


def unique(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if isinstance(value, str) and value and value not in result:
            result.append(value)
    return result


def as_id_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return unique([item for item in value if isinstance(item, str)])


def trim_text(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n...[truncated]"


def trim(text: str) -> dict[str, Any]:
    if len(text) <= MAX_FILE_CHARS:
        return {"content": text, "truncated": False, "chars": len(text)}
    return {"content": text[:MAX_FILE_CHARS], "truncated": True, "chars": len(text)}


def safe_read_text(path: str, session_id: str | None = None, max_chars: int = MAX_SCENE_SLICE_CHARS) -> str:
    try:
        return trim_text(read_project_or_runtime_file(path, session_id), max_chars)
    except Exception:
        return ""


def simple_yaml_value(text: str, key: str) -> str | None:
    pattern = re.compile(rf"^\s*{re.escape(key)}\s*:\s*[\"']?(.*?)[\"']?\s*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return None
    value = match.group(1).strip()
    return value or None


def deep_merge(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            base[key] = deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def parse_json_text(value: str) -> dict[str, Any]:
    if not value:
        return {}
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def read_json_state(session_id: str, filename: str) -> dict[str, Any]:
    value = read_state(session_id, filename)
    return value if isinstance(value, dict) else {}


def write_json_state(session_id: str, filename: str, patch: dict[str, Any]) -> None:
    current = read_json_state(session_id, filename)
    deep_merge(current, patch)
    current["updated_at"] = utc_now()
    write_state(session_id, filename, current)


def character_folder(character_id: str) -> str | None:
    return CHARACTER_FOLDERS.get(character_id)


def add_character_files(
    required_files: list[str],
    character_ids: list[str],
    *,
    level: Literal["light", "full", "goals", "details"] = "full",
) -> None:
    for character_id in character_ids:
        folder = character_folder(character_id)
        if not folder:
            continue
        if level == "light":
            required_files.extend(character_light_files(folder))
        elif level == "goals":
            required_files.extend(character_goal_files(folder))
        elif level == "details":
            required_files.extend(character_detail_files(folder))
        else:
            required_files.extend(character_core_files(folder))


def add_location_files(required_files: list[str], location_id: str | None) -> None:
    if not location_id:
        return
    required_files.extend(LOCATION_REQUIRED_FILES.get(location_id, []))


def should_load_goals(current_state: dict[str, Any], character_id: str) -> bool:
    ids = unique(
        as_id_list(current_state.get("goal_character_ids"))
        + as_id_list(current_state.get("initiator_character_ids"))
        + as_id_list(current_state.get("scene_driver_character_ids"))
    )
    return character_id in ids


def should_load_details(current_state: dict[str, Any], character_id: str) -> bool:
    detail_keys = [
        "detail_character_ids",
        "energy_character_ids",
        "habit_character_ids",
        "past_character_ids",
        "training_character_ids",
        "combat_character_ids",
        "close_interaction_character_ids",
    ]
    for key in detail_keys:
        if character_id in as_id_list(current_state.get(key)):
            return True

    scene_tags = as_id_list(current_state.get("scene_tags"))
    detail_tags = {"energy", "training", "combat", "sparring", "past", "memory", "medical", "injury"}
    return bool(set(scene_tags) & detail_tags)


def selected_character_ids(current_state: dict[str, Any]) -> dict[str, list[str]]:
    pov_id = current_state.get("pov_character_id")
    active = as_id_list(current_state.get("active_character_ids"))
    nearby = as_id_list(current_state.get("nearby_character_ids"))
    mentioned = as_id_list(current_state.get("mentioned_character_ids"))
    scheduled = as_id_list(current_state.get("scheduled_character_ids"))
    delayed = as_id_list(current_state.get("delayed_character_ids"))

    full = unique(([pov_id] if isinstance(pov_id, str) else []) + active + nearby)
    reference = unique(mentioned + scheduled + delayed)
    reference = [cid for cid in reference if cid not in full]

    return {
        "full": full,
        "reference": reference,
        "active": active,
        "nearby": nearby,
        "mentioned": mentioned,
        "scheduled": scheduled,
        "delayed": delayed,
    }


def build_required_files(current_state: dict[str, Any], mode: str) -> list[str]:
    required_files = list(CORE_REQUIRED_FILES)

    arc_id = current_state.get("current_arc_id") or "arc_001_academy_start"
    if isinstance(arc_id, str) and arc_id:
        required_files.append(f"story/arcs/{arc_id}.yaml")

    location_id = current_state.get("current_location_id") or "loc_academy_main"
    add_location_files(required_files, location_id)

    selected = selected_character_ids(current_state)
    add_character_files(required_files, selected["full"], level="full")
    add_character_files(required_files, selected["reference"], level="light")

    for character_id in selected["full"]:
        if should_load_goals(current_state, character_id):
            add_character_files(required_files, [character_id], level="goals")
        if should_load_details(current_state, character_id):
            add_character_files(required_files, [character_id], level="details")

    if mode in {"technical", "audit", "transfer"}:
        required_files.extend(TECHNICAL_EXTRA_FILES)

    if mode in {"audit", "transfer"}:
        required_files.extend(AUDIT_EXTRA_FILES)

    return unique(required_files)


def relationship_participants(key: str, value: Any) -> list[str]:
    if isinstance(value, dict):
        for field in ("characters", "participants", "character_ids"):
            ids = as_id_list(value.get(field))
            if ids:
                return ids
    return unique(re.findall(r"char_[A-Za-z0-9_]+", key))


def build_relationship_slice(session_id: str, scene_ids: list[str]) -> dict[str, Any]:
    relationships = read_json_state(session_id, "relationships.json")
    result: dict[str, Any] = {}
    for key, value in relationships.items():
        participants = relationship_participants(key, value)
        if len([cid for cid in participants if cid in scene_ids]) >= 2:
            result[key] = value
    return result


def build_knowledge_slice(session_id: str, scene_ids: list[str]) -> dict[str, Any]:
    knowledge = read_json_state(session_id, "knowledge_state.json")
    return {cid: knowledge.get(cid, {}) for cid in scene_ids if cid in knowledge}


def build_open_threads_slice(session_id: str, scene_ids: list[str]) -> dict[str, Any]:
    open_threads = read_json_state(session_id, "open_threads.json")
    result: dict[str, Any] = {}
    for key, value in open_threads.items():
        if not isinstance(value, dict):
            continue
        status = value.get("status", "open")
        participants = as_id_list(value.get("participants")) or as_id_list(value.get("character_ids"))
        if status in {"closed", "resolved", "archived"}:
            continue
        if participants and any(cid in scene_ids for cid in participants):
            result[key] = value
        elif not participants and len(result) < 8:
            result[key] = value
    return result


def build_shared_incidents_slice(session_id: str, scene_ids: list[str]) -> dict[str, Any]:
    incidents = read_json_state(session_id, "shared_incidents.json")
    result: dict[str, Any] = {}
    for key, value in incidents.items():
        if not isinstance(value, dict):
            continue
        participants = unique(
            as_id_list(value.get("participants"))
            + as_id_list(value.get("witnesses"))
            + as_id_list(value.get("known_by"))
        )
        status = value.get("status", "active_reference")
        if participants and any(cid in scene_ids for cid in participants) and status != "archived":
            result[key] = value
        if len(result) >= 10:
            break
    return result


def item_related_to_scene(value: Any, scene_ids: list[str], location_id: str | None, date_value: str | None) -> bool:
    if not isinstance(value, dict):
        return False

    chars = unique(
        as_id_list(value.get("characters"))
        + as_id_list(value.get("participants"))
        + as_id_list(value.get("about"))
        + as_id_list(value.get("witnesses"))
        + as_id_list(value.get("required_characters"))
        + as_id_list(value.get("characters_required"))
        + as_id_list(value.get("characters_optional"))
    )

    if chars and any(cid in scene_ids for cid in chars):
        return True

    locs = unique(
        as_id_list(value.get("location_ids"))
        + as_id_list(value.get("location_tags"))
    )
    loc_single = value.get("location_id")
    if isinstance(loc_single, str):
        locs.append(loc_single)
    if location_id and location_id in locs:
        return True

    for date_key in ("date", "current_date", "starts_at", "created_at"):
        raw = value.get(date_key)
        if isinstance(raw, str) and date_value and raw.startswith(date_value):
            return True
        if isinstance(raw, dict):
            raw_date = raw.get("date")
            if isinstance(raw_date, str) and raw_date == date_value:
                return True

    return False


def slice_state_items(
    state: dict[str, Any],
    scene_ids: list[str],
    location_id: str | None,
    date_value: str | None,
    *,
    statuses: set[str] | None = None,
    max_items: int = 12,
) -> dict[str, Any]:
    result: dict[str, Any] = {}

    for key, value in state.items():
        if not isinstance(value, dict):
            continue

        if statuses is not None:
            status = str(value.get("status", "active"))
            if status not in statuses:
                continue

        if item_related_to_scene(value, scene_ids, location_id, date_value):
            result[key] = value
        elif len(result) < 3 and str(value.get("priority", "")).isdigit() and int(value.get("priority", 0)) >= 4:
            result[key] = value

        if len(result) >= max_items:
            break

    return result


def build_event_engine_slice(session_id: str, current_state: dict[str, Any], scene_ids: list[str]) -> dict[str, Any]:
    location_id = current_state.get("current_location_id")
    if not isinstance(location_id, str):
        location_id = None

    date_value = current_state.get("current_date")
    if not isinstance(date_value, str):
        date_value = None

    event_seeds = read_json_state(session_id, "event_seeds.json")
    event_queue = read_json_state(session_id, "event_queue.json")
    director_notes = read_json_state(session_id, "director_notes.json")
    gossip_state = read_json_state(session_id, "gossip_state.json")
    rating_state = read_json_state(session_id, "rating_state.json")
    energy_incidents = read_json_state(session_id, "energy_incidents.json")

    rating_slice = {
        cid: rating_state.get(cid, {})
        for cid in scene_ids
        if isinstance(rating_state.get(cid, {}), dict)
    }

    active_focus = director_notes.get("current_director_focus", [])
    if not isinstance(active_focus, list):
        active_focus = []

    return {
        "rules_source": "engine/event_engine_rules.md",
        "director_notes": {
            "current_director_focus": active_focus[:5],
            "note": "Use as hidden planning guidance. Do not show director notes to the user.",
        },
        "event_seeds": slice_state_items(
            event_seeds,
            scene_ids,
            location_id,
            date_value,
            statuses={"seeded", "active", "maturing"},
            max_items=10,
        ),
        "event_queue": slice_state_items(
            event_queue,
            scene_ids,
            location_id,
            date_value,
            statuses={"pending", "ready", "active"},
            max_items=10,
        ),
        "gossip_state": slice_state_items(
            gossip_state,
            scene_ids,
            location_id,
            date_value,
            statuses={"active", "spreading", "new"},
            max_items=10,
        ),
        "rating_state": rating_slice,
        "energy_incidents": slice_state_items(
            energy_incidents,
            scene_ids,
            location_id,
            date_value,
            statuses={"active", "pending", "recent", "resolved_scene_hook"},
            max_items=8,
        ),
        "selection_protocol": [
            "First follow the current calendar beat.",
            "Then choose one suitable queued event or seed if it matches current place, characters and pacing.",
            "If no suitable event exists, create one small seed from visible scene behavior.",
            "Do not reveal director notes to the user.",
            "After scene, save new seeds, queued events, gossip, rating or energy incident changes through applyTurnResultSimple.",
        ],
        "event_palette": [
            "gossip",
            "jealousy",
            "provocation",
            "rating_pressure",
            "energy_flare",
            "minor_fight",
            "social_attention",
            "instructor_note",
            "mistake_with_consequence",
            "unexpected_character_entry",
            "quiet_observation_that_later_matters",
        ],
    }


def extract_calendar_day_block(calendar_text: str, day_id: str | None, date_value: str | None) -> str:
    lines = calendar_text.splitlines()
    start: int | None = None

    if day_id:
        pattern = f"  {day_id}:"
        for i, line in enumerate(lines):
            if line.startswith(pattern):
                start = i
                break

    if start is None and date_value:
        for i, line in enumerate(lines):
            if f'date: "{date_value}"' in line or f"date: '{date_value}'" in line or f"date: {date_value}" in line:
                for j in range(i, -1, -1):
                    if re.match(r"^  [A-Za-z0-9_]+:\s*$", lines[j]):
                        start = j
                        break
                break

    if start is None:
        return ""

    end = len(lines)
    for j in range(start + 1, len(lines)):
        if re.match(r"^  [A-Za-z0-9_]+:\s*$", lines[j]):
            end = j
            break

    return "\n".join(lines[start:end])


def build_calendar_slice(session_id: str, current_state: dict[str, Any]) -> dict[str, Any]:
    calendar_id = current_state.get("current_calendar_id") or "academy_start"
    current_day_id = current_state.get("current_day_id")
    current_date = current_state.get("current_date")

    source_file = f"story/calendar/{calendar_id}.yaml"
    calendar_text = safe_read_text(source_file, session_id, max_chars=50000)
    day_block = extract_calendar_day_block(
        calendar_text,
        current_day_id if isinstance(current_day_id, str) else None,
        current_date if isinstance(current_date, str) else None,
    )

    protocol = ""
    if "calendar_reading_protocol:" in calendar_text:
        protocol = trim_text(calendar_text.split("\ndays:", 1)[0], 2500)

    return {
        "source_file": source_file,
        "calendar_id": calendar_id,
        "current_day_id": current_day_id,
        "current_date": current_date,
        "protocol": protocol,
        "current_day_block": trim_text(day_block, 6000),
        "selection_rule": "Use only current_day_block for this turn unless the player explicitly skips time or asks for calendar audit.",
    }


def format_date_human(date_value: Any, weekday_value: Any) -> str:
    if not isinstance(date_value, str):
        return ""
    parts = date_value.split("-")
    if len(parts) != 3:
        return date_value

    try:
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
    except ValueError:
        return date_value

    month_name = MONTHS_RU.get(month, parts[1])
    weekday = WEEKDAY_SHORT.get(str(weekday_value or "").lower(), str(weekday_value or "").lower())
    if weekday:
        return f"{day} {month_name} {weekday} {year}"
    return f"{day} {month_name} {year}"


def format_time_human(time_value: Any, time_of_day: Any) -> str:
    tod = TIME_OF_DAY_RU.get(str(time_of_day or "").lower(), str(time_of_day or ""))
    if isinstance(time_value, str) and time_value:
        if tod:
            return f"{tod}, около {time_value}"
        return f"около {time_value}"
    return tod


def format_weather_human(weather: Any) -> str:
    if not isinstance(weather, dict):
        return ""
    parts: list[str] = []
    condition = weather.get("condition")
    temp = weather.get("temperature_c")
    wind = weather.get("wind")
    precipitation = weather.get("precipitation")
    ground = weather.get("ground")

    if condition:
        parts.append(str(condition))
    if temp is not None:
        parts.append(f"{temp}°C")
    if wind:
        parts.append(str(wind))
    if precipitation and precipitation not in {"нет", "none", "no"}:
        parts.append(str(precipitation))
    if ground:
        parts.append(str(ground))
    return ", ".join(parts)


def format_pov_state_human(current_state: dict[str, Any]) -> str:
    pov_id = current_state.get("pov_character_id", "char_akira")
    status = {}
    if isinstance(current_state.get("character_status"), dict):
        status = current_state.get("character_status", {}).get(pov_id, {}) or {}

    bits: list[str] = []

    physical_state = status.get("physical_state")
    if physical_state:
        bits.append(str(physical_state))

    pain = status.get("pain")
    injuries = status.get("injuries")
    if pain:
        bits.append(f"боль: {pain}")
    if isinstance(injuries, list) and injuries:
        bits.append("травмы: " + ", ".join(str(item) for item in injuries))
    elif not pain:
        bits.append("без травм")

    fatigue = status.get("fatigue")
    if isinstance(fatigue, (int, float)) and fatigue > 0:
        bits.append(f"усталость {fatigue}/10")

    clothing_state = status.get("clothing_state")
    hair_state = status.get("hair_state")
    if clothing_state:
        bits.append(str(clothing_state))
    if hair_state:
        bits.append(str(hair_state))

    return "; ".join(bits)


def format_context_human(current_state: dict[str, Any], location_text: str) -> str:
    pieces: list[str] = []

    visible_items = current_state.get("scene_continuity", {}).get("visible_item_state") if isinstance(current_state.get("scene_continuity"), dict) else {}
    if isinstance(visible_items, dict):
        for key, value in visible_items.items():
            if value:
                pieces.append(str(value) if not isinstance(value, bool) else str(key))

    nearby = as_id_list(current_state.get("nearby_character_ids"))
    active = as_id_list(current_state.get("active_character_ids"))
    pov = current_state.get("pov_character_id")
    scene_people = [cid for cid in unique(active + nearby) if cid != pov]
    if scene_people:
        readable = [cid.replace("char_", "") for cid in scene_people]
        pieces.extend(readable)

    context_line = simple_yaml_value(location_text, "header_context")
    if context_line:
        pieces.append(context_line)

    return ", ".join(unique([p for p in pieces if p]))


def location_human(session_id: str | None, location_id: Any) -> dict[str, str]:
    if not isinstance(location_id, str):
        return {"location_id": "", "display_name": "", "header_name": "", "short_name": "", "raw_card": ""}

    files = LOCATION_REQUIRED_FILES.get(location_id, [])
    card_path = files[0] if files else ""
    text = safe_read_text(card_path, session_id, max_chars=2500) if card_path else ""

    display = simple_yaml_value(text, "display_name") or location_id
    header = simple_yaml_value(text, "header_name") or display
    short = simple_yaml_value(text, "short_name") or display

    return {
        "location_id": location_id,
        "display_name": display,
        "header_name": header,
        "short_name": short,
        "raw_card": text,
    }


def build_current_frame(current_state: dict[str, Any], session_id: str | None = None) -> dict[str, Any]:
    pov_id = current_state.get("pov_character_id", "char_akira")
    status = {}
    if isinstance(current_state.get("character_status"), dict):
        status = current_state.get("character_status", {}).get(pov_id, {}) or {}

    loc = location_human(session_id, current_state.get("current_location_id"))
    weather_human = format_weather_human(current_state.get("weather", {}))
    date_human = format_date_human(current_state.get("current_date"), current_state.get("current_day_of_week"))
    time_human = format_time_human(current_state.get("current_time"), current_state.get("time_of_day"))
    pov_state_human = format_pov_state_human(current_state)
    context_human = format_context_human(current_state, loc.get("raw_card", ""))

    return {
        "date": current_state.get("current_date"),
        "day_of_week": current_state.get("current_day_of_week"),
        "time": current_state.get("current_time"),
        "time_of_day": current_state.get("time_of_day"),
        "location_id": current_state.get("current_location_id"),
        "location_display_name": loc.get("display_name"),
        "location_header_name": loc.get("header_name"),
        "location_short_name": loc.get("short_name"),
        "arc_id": current_state.get("current_arc_id"),
        "calendar_id": current_state.get("current_calendar_id"),
        "day_id": current_state.get("current_day_id"),
        "weather": current_state.get("weather", {}),
        "pov_character_id": pov_id,
        "pov_status": status,
        "active_character_ids": as_id_list(current_state.get("active_character_ids")),
        "nearby_character_ids": as_id_list(current_state.get("nearby_character_ids")),
        "mentioned_character_ids": as_id_list(current_state.get("mentioned_character_ids")),
        "scheduled_character_ids": as_id_list(current_state.get("scheduled_character_ids")),
        "delayed_character_ids": as_id_list(current_state.get("delayed_character_ids")),
        "header_values": {
            "date_human": date_human,
            "time_human": time_human,
            "location_human": loc.get("header_name"),
            "weather_human": weather_human,
            "pov_state_human": pov_state_human,
            "context_human": context_human,
        },
    }


def header_contract() -> dict[str, Any]:
    return {
        "priority": "highest_for_header",
        "template_lines": [
            "📅 {date_human}",
            "🕒 {time_human}",
            "📍 Место: {location_human}",
            "🌤 Погода: {weather_human}",
            "🫀 Состояние Акиры: {pov_state_human}",
            "🎒 При себе / рядом: {context_human}",
        ],
        "omit_empty_lines": True,
        "max_lines": 6,
        "rules": [
            "Use scene_contract.current_frame.header_values.",
            "Keep the header in this emoji format.",
            "Do not translate location names to English.",
            "If context_human is empty, omit the 🎒 line.",
            "The 🎒 line must be short: important carried items, nearby people or important scene objects only.",
        ],
    }


def response_format_contract() -> dict[str, Any]:
    return {
        "priority": "highest_for_scene_output",
        "scene_header_required": True,
        "header_contract": header_contract(),
        "meta_layer_forbidden": True,
        "allowed_response_parts": [
            "emoji header",
            "scene body",
            "choice block",
            "speech options",
            "POV thoughts block",
        ],
        "dialogue_format": "**Имя или видимый дескриптор** — Реплика. (*короткая ремарка: тон, взгляд, пауза, жест*)",
        "description_format": "*Описание действия, окружения или атмосферы отдельной строкой курсивом.*",
        "scene_body_rules": [
            "Use visible POV only.",
            "No assistant commentary before or after the scene.",
            "No comments about saving, API, Actions, state or turn-contract in play response.",
            "No direct inner thoughts in scene body.",
            "NPC thoughts are not facts.",
            "Known names only after POV knows them.",
            "Descriptions and atmosphere go as separate italic paragraphs.",
            "Dialogue uses bold speaker tag and long dash.",
        ],
        "ending_block": [
            "━━━━━━━━━━━━━━━━━━━━",
            "Что можно сделать:",
            "1.",
            "2.",
            "3.",
            "",
            "Что сказать:",
            "— “...”",
            "— “...”",
            "— “...”",
            "",
            "Мысли Акиры:",
            "— ...",
            "— ...",
            "— ...",
            "━━━━━━━━━━━━━━━━━━━━",
        ],
        "self_check": "If the response is not in this format, rewrite it before sending.",
    }


def scene_density_contract() -> dict[str, Any]:
    return {
        "target_scene_beats": "3-5",
        "minimum_scene_units": "5-9 short paragraphs/units unless pure transition",
        "minimum_for_meaningful_scene": [
            "environment or academy system in motion",
            "visible POV observation, not passive empty standing",
            "at least one active/nearby character-specific reaction, line, mistake, provocation or social move",
            "one concrete change: knowledge, position, tension, schedule, access, reputation, body/clothing state or open thread",
            "one event-engine element if fitting: gossip, rating, jealousy, provocation, energy flare, minor fight, instructor note or delayed character entry",
            "stop at a real intervention point",
        ],
        "do_not_stop_after": [
            "pure scenery setup",
            "one vague question with no pressure",
            "a decorative weather sentence only",
            "procedural registration instruction",
        ],
        "allowed_short_scene": "Only for pure transition with no event; then summarize and move to nearest meaningful beat.",
    }


def build_scene_contract(session_id: str, current_state: dict[str, Any], mode: str) -> dict[str, Any]:
    selected = selected_character_ids(current_state)
    scene_ids = unique(selected["full"])

    arc_id = current_state.get("current_arc_id") or "arc_001_academy_start"
    arc_file = f"story/arcs/{arc_id}.yaml"

    location_id = current_state.get("current_location_id") or "loc_academy_main"
    location_files = LOCATION_REQUIRED_FILES.get(location_id, [])

    current_frame = build_current_frame(current_state, session_id)

    return {
        "version": "scene_contract_v2_event_engine",
        "mode": mode,
        "current_frame": current_frame,
        "header_contract": header_contract(),
        "calendar_slice": build_calendar_slice(session_id, current_state),
        "arc_slice": {
            "source_file": arc_file,
            "content": safe_read_text(arc_file, session_id, max_chars=5000),
        },
        "location_slice": {
            "location_id": location_id,
            "source_files": location_files,
            "content": {
                path: safe_read_text(path, session_id, max_chars=2500)
                for path in location_files
            },
        },
        "character_load_plan": {
            "full_character_ids": selected["full"],
            "reference_character_ids": selected["reference"],
            "full_rule": "Full files are loaded only for POV/active/nearby characters.",
            "reference_rule": "Mentioned/scheduled/delayed characters use light info unless they enter the scene.",
            "active_character_file_rule": "For every full character, behavior.md and voice.md must be used. If missing from contract, fetch them through getProjectFileByQuery before writing scene.",
        },
        "relationship_slice": build_relationship_slice(session_id, scene_ids),
        "knowledge_slice": build_knowledge_slice(session_id, scene_ids),
        "open_threads_slice": build_open_threads_slice(session_id, scene_ids),
        "shared_incidents_slice": build_shared_incidents_slice(session_id, scene_ids),
        "event_engine_slice": build_event_engine_slice(session_id, current_state, scene_ids),
        "response_format_contract": response_format_contract(),
        "scene_density_contract": scene_density_contract(),
        "selection_rules": [
            "Do not load every project file for a normal scene.",
            "Use current calendar day only unless time skip/audit requires more.",
            "Use full character files only for POV/active/nearby characters.",
            "For full characters, use behavior.md and voice.md; fetch them by query if missing.",
            "Use light character info for mentioned/scheduled/delayed characters.",
            "Use relationships, knowledge and incidents only for characters present or directly affecting the current beat.",
            "Use event_engine_slice to create interesting scene pressure between calendar points.",
        ],
    }


@app.on_event("startup")
def startup() -> None:
    ensure_runtime_root()


@app.get("/")
def root() -> dict[str, Any]:
    return {
        "status": "ok",
        "project": PROJECT_SLUG,
        "version": "3.2.1",
        "actions_schema": "/openapi-actions.json",
        "health": "/health",
        "debug_volume": "/debug/volume",
    }


@app.get("/health")
def health() -> dict[str, Any]:
    return {"success": True, "project": PROJECT_SLUG, "version": "3.2.1", "time": utc_now()}


@app.get("/debug/volume")
def debug_volume() -> dict[str, Any]:
    try:
        return {"success": True, **debug_info()}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/api/v1/sessions")
def create_session(req: CreateSessionRequest | None = None) -> dict[str, Any]:
    req = req or CreateSessionRequest()
    sid, root_dir = ensure_session(req.session_id, reset=req.reset)
    return {
        "success": True,
        "session_id": sid,
        "session_root": str(root_dir),
        "state_root": str(session_state_root(sid)),
        "reset": req.reset,
        "next": {"turn_contract": f"/api/v1/sessions/{sid}/turn-contract"},
    }


@app.post("/api/v1/sessions/{session_id}/turn-contract")
def get_turn_contract(session_id: str, req: TurnContractRequest) -> dict[str, Any]:
    sid, _ = ensure_session(session_id, reset=False)
    current_state = read_json_state(sid, "current_state.json")
    required_files = build_required_files(current_state, req.mode)
    scene_contract = build_scene_contract(sid, current_state, req.mode)

    contents: dict[str, Any] = {}
    if req.include_file_contents:
        for path in required_files:
            try:
                contents[path] = trim(read_project_or_runtime_file(path, sid))
            except Exception as exc:
                contents[path] = {"error": str(exc), "truncated": False, "chars": 0, "content": ""}

    return {
        "success": True,
        "session_id": sid,
        "mode": req.mode,
        "is_game_turn": req.mode == "play",
        "current_state": current_state,
        "scene_contract": scene_contract,
        "required_files": required_files,
        "required_file_contents": contents,
        "checks": [
            "Novel director has top priority: write a living interactive scene, not a registration instruction.",
            "Use scene_contract first; required_files are support, not the whole project.",
            "Use event_engine_slice to create interesting events between calendar points.",
            "Do not reveal director notes to user.",
            "Default play turn calls should use include_file_contents=false to avoid ResponseTooLargeError.",
            "Use scene_contract.header_contract and current_frame.header_values for the header.",
            "Do not translate location names to English; use location_human.",
            "Use current calendar slice only unless time skip/audit requires more.",
            "Use full character files only for POV/active/nearby characters.",
            "For full characters, use behavior.md and voice.md; fetch them by query if missing.",
            "Use light info for mentioned/scheduled/delayed characters.",
            "Use relationship/knowledge slices from scene_contract before NPC claims.",
            "Obey response_format_contract and scene_density_contract.",
            "After a meaningful scene, call applyTurnResult or applyTurnResultSimple.",
        ],
    }


@app.post("/api/v1/sessions/{session_id}/apply-turn-result")
def apply_turn_result(session_id: str, req: ApplyTurnResultRequest) -> dict[str, Any]:
    sid, _ = ensure_session(session_id, reset=False)
    state_root = session_state_root(sid)

    if req.technical:
        append_jsonl(
            session_root(sid) / "technical_history.jsonl",
            {"time": utc_now(), "scene_id": req.scene_id, "text": req.scene_text},
        )
        return {"success": True, "status": "technical_saved", "session_id": sid}

    append_jsonl(
        state_root / "scene_history.jsonl",
        {"time": utc_now(), "scene_id": req.scene_id, "scene_text": req.scene_text},
    )

    patch_map = [
        ("current_state.json", req.current_state_changes),
        ("knowledge_state.json", req.knowledge_changes),
        ("relationships.json", req.relationship_changes),
        ("open_threads.json", req.open_thread_changes),
        ("shared_incidents.json", req.shared_incident_changes),
        ("inventory_state.json", req.inventory_changes),
        ("event_seeds.json", req.event_seed_changes),
        ("event_queue.json", req.event_queue_changes),
        ("director_notes.json", req.director_note_changes),
        ("gossip_state.json", req.gossip_changes),
        ("rating_state.json", req.rating_changes),
        ("energy_incidents.json", req.energy_incident_changes),
    ]

    updated = ["scene_history.jsonl"]

    for filename, patch in patch_map:
        if patch:
            write_json_state(sid, filename, patch)
            updated.append(filename)

    for character_id, patch in req.character_memory_changes.items():
        if isinstance(patch, dict):
            path = state_root / "character_memory" / f"{character_id}.json"
            current = read_json(path, {})
            if not isinstance(current, dict):
                current = {}
            deep_merge(current, patch)
            current.setdefault("character_id", character_id)
            current["updated_at"] = utc_now()
            write_json_atomic(path, current)
            updated.append(f"character_memory/{character_id}.json")

    compaction = read_json_state(sid, "compaction_state.json")
    compaction["total_game_turns"] = int(compaction.get("total_game_turns", 0) or 0) + 1
    compaction["since_last_compaction"] = int(compaction.get("since_last_compaction", 0) or 0) + 1
    compaction["compact_every_turns"] = int(
        compaction.get("compact_every_turns", COMPACT_EVERY_TURNS) or COMPACT_EVERY_TURNS
    )
    compaction["needs_compaction"] = compaction["since_last_compaction"] >= compaction["compact_every_turns"]
    compaction["last_scene_id"] = req.scene_id
    compaction["updated_at"] = utc_now()

    write_state(sid, "compaction_state.json", compaction)
    updated.append("compaction_state.json")

    return {
        "success": True,
        "session_id": sid,
        "updated_files": updated,
        "needs_compaction": compaction.get("needs_compaction", False),
    }


@app.post("/api/v1/sessions/{session_id}/apply-turn-result-simple")
def apply_turn_result_simple(session_id: str, req: ApplyTurnResultSimpleRequest) -> dict[str, Any]:
    return apply_turn_result(
        session_id,
        ApplyTurnResultRequest(
            scene_id=req.scene_id,
            scene_text=req.scene_text,
            technical=req.technical,
            current_state_changes=parse_json_text(req.current_state_changes_json),
            knowledge_changes=parse_json_text(req.knowledge_changes_json),
            relationship_changes=parse_json_text(req.relationship_changes_json),
            open_thread_changes=parse_json_text(req.open_thread_changes_json),
            shared_incident_changes=parse_json_text(req.shared_incident_changes_json),
            inventory_changes=parse_json_text(req.inventory_changes_json),
            character_memory_changes=parse_json_text(req.character_memory_changes_json),
            event_seed_changes=parse_json_text(req.event_seed_changes_json),
            event_queue_changes=parse_json_text(req.event_queue_changes_json),
            director_note_changes=parse_json_text(req.director_note_changes_json),
            gossip_changes=parse_json_text(req.gossip_changes_json),
            rating_changes=parse_json_text(req.rating_changes_json),
            energy_incident_changes=parse_json_text(req.energy_incident_changes_json),
        ),
    )


@app.post("/api/v1/sessions/{session_id}/compact")
def compact_session(session_id: str, req: CompactRequest) -> dict[str, Any]:
    sid, _ = ensure_session(session_id, reset=False)

    if req.recent_turns_md is not None:
        write_state(sid, "recent_turns.md", req.recent_turns_md)

    for filename, patch in req.state_updates.items():
        if isinstance(patch, dict) and filename.endswith(".json"):
            write_json_state(sid, filename, patch)

    compaction = read_json_state(sid, "compaction_state.json")
    compaction["last_compaction_at"] = utc_now()
    compaction["last_compaction_reason"] = req.reason
    compaction["since_last_compaction"] = 0
    compaction["needs_compaction"] = False

    write_state(sid, "compaction_state.json", compaction)

    return {"success": True, "session_id": sid, "status": "compacted"}


@app.get("/api/v1/sessions/{session_id}/state/{filename}")
def read_session_state_file(session_id: str, filename: str) -> PlainTextResponse:
    try:
        safe_filename = safe_repo_path(filename)
        text = read_project_or_runtime_file(f"state/{safe_filename}", session_id)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return PlainTextResponse(text)


@app.get("/api/v1/files/{file_path:path}")
def read_file(file_path: str, session_id: str | None = None) -> PlainTextResponse:
    try:
        text = read_project_or_runtime_file(safe_repo_path(file_path), session_id)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return PlainTextResponse(text)


@app.get("/api/v1/file")
def read_file_query(path: str = Query(...), session_id: str | None = None) -> PlainTextResponse:
    try:
        text = read_project_or_runtime_file(safe_repo_path(path), session_id)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return PlainTextResponse(text)


@app.get("/openapi-actions.json")
def openapi_actions() -> dict[str, Any]:
    server = PUBLIC_BASE_URL or "https://your-service.up.railway.app"

    return {
        "openapi": "3.1.0",
        "info": {"title": f"{PROJECT_SLUG} GPT Actions", "version": "3.2.1"},
        "servers": [{"url": server}],
        "paths": {
            "/health": {
                "get": {
                    "operationId": "healthCheck",
                    "summary": "Check API health",
                    "responses": {"200": {"description": "OK"}},
                }
            },
            "/debug/volume": {
                "get": {
                    "operationId": "debugVolume",
                    "summary": "Check runtime volume",
                    "responses": {"200": {"description": "OK"}},
                }
            },
            "/api/v1/sessions": {
                "post": {
                    "operationId": "createSession",
                    "summary": "Create a new runtime session",
                    "requestBody": {
                        "required": False,
                        "content": {"application/json": {"schema": CreateSessionRequest.model_json_schema()}},
                    },
                    "responses": {"200": {"description": "Session created"}},
                }
            },
            "/api/v1/sessions/{session_id}/turn-contract": {
                "post": {
                    "operationId": "getSessionTurnContract",
                    "summary": "Get compact smart scene contract for one turn",
                    "parameters": [
                        {"name": "session_id", "in": "path", "required": True, "schema": {"type": "string"}}
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {"application/json": {"schema": TurnContractRequest.model_json_schema()}},
                    },
                    "responses": {"200": {"description": "Smart turn contract"}},
                }
            },
            "/api/v1/file": {
                "get": {
                    "operationId": "getProjectFileByQuery",
                    "summary": "Read one project or runtime file by query path",
                    "parameters": [
                        {"name": "path", "in": "query", "required": True, "schema": {"type": "string"}},
                        {"name": "session_id", "in": "query", "required": False, "schema": {"type": "string"}},
                    ],
                    "responses": {"200": {"description": "Project or runtime file"}},
                }
            },
            "/api/v1/files/{file_path}": {
                "get": {
                    "operationId": "getProjectFile",
                    "summary": "Read one project or runtime file by path",
                    "parameters": [
                        {"name": "file_path", "in": "path", "required": True, "schema": {"type": "string"}},
                        {"name": "session_id", "in": "query", "required": False, "schema": {"type": "string"}},
                    ],
                    "responses": {"200": {"description": "Project or runtime file"}},
                }
            },
            "/api/v1/sessions/{session_id}/apply-turn-result": {
                "post": {
                    "operationId": "applyTurnResult",
                    "summary": "Persist scene and state changes",
                    "parameters": [
                        {"name": "session_id", "in": "path", "required": True, "schema": {"type": "string"}}
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {"application/json": {"schema": ApplyTurnResultRequest.model_json_schema()}},
                    },
                    "responses": {"200": {"description": "Saved"}},
                }
            },
            "/api/v1/sessions/{session_id}/apply-turn-result-simple": {
                "post": {
                    "operationId": "applyTurnResultSimple",
                    "summary": "Persist scene and state changes using JSON strings for GPT Actions",
                    "parameters": [
                        {"name": "session_id", "in": "path", "required": True, "schema": {"type": "string"}}
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {"application/json": {"schema": ApplyTurnResultSimpleRequest.model_json_schema()}},
                    },
                    "responses": {"200": {"description": "Saved"}},
                }
            },
            "/api/v1/sessions/{session_id}/compact": {
                "post": {
                    "operationId": "compactSessionMemory",
                    "summary": "Persist memory compaction",
                    "parameters": [
                        {"name": "session_id", "in": "path", "required": True, "schema": {"type": "string"}}
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {"application/json": {"schema": CompactRequest.model_json_schema()}},
                    },
                    "responses": {"200": {"description": "Compacted"}},
                }
            },
            "/api/v1/sessions/{session_id}/state/{filename}": {
                "get": {
                    "operationId": "getSessionStateFile",
                    "summary": "Read one runtime state file",
                    "parameters": [
                        {"name": "session_id", "in": "path", "required": True, "schema": {"type": "string"}},
                        {"name": "filename", "in": "path", "required": True, "schema": {"type": "string"}},
                    ],
                    "responses": {"200": {"description": "State file"}},
                }
            },
        },
    }
