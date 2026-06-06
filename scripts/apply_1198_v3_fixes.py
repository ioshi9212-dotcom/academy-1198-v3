from __future__ import annotations

from pathlib import Path


def find_repo_root() -> Path:
    candidates = [Path.cwd(), Path(__file__).resolve().parents[1], Path(__file__).resolve().parents[2]]
    for root in candidates:
        if (root / "app" / "main.py").exists():
            return root
    raise SystemExit("Не нашла app/main.py. Запусти скрипт из корня academy-1198-v3.")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"Не смогла применить блок: {label}. Файл app/main.py уже отличается — открой PATCHES/app_main_runtime_slices_and_json_validation.patch и примени вручную.")
    return text.replace(old, new, 1)


def patch_app_main(root: Path) -> None:
    path = root / "app" / "main.py"
    text = path.read_text(encoding="utf-8")

    old_core = '''CORE_REQUIRED_FILES = [
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
'''
    new_core = '''CORE_REQUIRED_FILES = [
    "MANCHESS_RULES.md",
    "engine/turn_contract.md",
    "engine/loading_policy.md",
    "engine/source_priority.md",
    "engine/current_frame_policy.md",
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
    "world/academy/academy_index.yaml",
    "knowledge/knowledge_rules.md",
]
'''
    text = replace_once(text, old_core, new_core, "CORE_REQUIRED_FILES")

    old_state_helpers = '''def parse_json_text(value: str) -> dict[str, Any]:
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
'''
    new_state_helpers = '''ROOT_METADATA_KEYS = {"schema", "session_id", "updated_at", "description"}
STATE_ITEM_CONTAINER_KEYS = {
    "relationships.json": "relationships",
    "open_threads.json": "threads",
    "shared_incidents.json": "incidents",
    "event_seeds.json": "items",
    "event_queue.json": "items",
    "gossip_state.json": "items",
    "energy_incidents.json": "items",
}


def parse_json_text(value: str, field_name: str = "json") -> dict[str, Any]:
    if value is None or not str(value).strip():
        return {}
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid JSON in {field_name}: {exc.msg} at line {exc.lineno}, column {exc.colno}",
        ) from exc
    if not isinstance(parsed, dict):
        raise HTTPException(status_code=400, detail=f"Invalid JSON in {field_name}: expected JSON object")
    return parsed


def read_json_state(session_id: str, filename: str) -> dict[str, Any]:
    value = read_state(session_id, filename)
    return value if isinstance(value, dict) else {}


def state_container_items(state: dict[str, Any], container_key: str) -> dict[str, Any]:
    """Return focused runtime items from both the new container format and legacy top-level format."""
    result: dict[str, Any] = {}
    nested = state.get(container_key)
    if isinstance(nested, dict):
        result.update(nested)

    for key, value in state.items():
        if key == container_key or key in ROOT_METADATA_KEYS:
            continue
        if isinstance(value, dict):
            result.setdefault(key, value)
    return result


def normalize_container_patch(patch: dict[str, Any], container_key: str) -> dict[str, Any]:
    if not patch:
        return {}

    normalized: dict[str, Any] = {
        key: value for key, value in patch.items() if key in ROOT_METADATA_KEYS
    }
    items: dict[str, Any] = {}

    nested = patch.get(container_key)
    if isinstance(nested, dict):
        items.update(nested)

    for key, value in patch.items():
        if key == container_key or key in ROOT_METADATA_KEYS:
            continue
        items[key] = value

    if items:
        normalized[container_key] = items
    return normalized or patch


def normalize_knowledge_patch(patch: dict[str, Any]) -> dict[str, Any]:
    if not patch:
        return {}

    root_keys = ROOT_METADATA_KEYS | {
        "public_knowledge",
        "hidden_truths",
        "character_knowledge",
        "evidence_log",
        "speaker_labels",
    }
    normalized: dict[str, Any] = {
        key: value for key, value in patch.items() if key in root_keys
    }
    character_items: dict[str, Any] = {}

    for key, value in patch.items():
        if key in root_keys:
            continue
        if isinstance(key, str) and key.startswith("char_") and isinstance(value, dict):
            character_items[key] = value
        else:
            normalized[key] = value

    if character_items:
        existing = normalized.get("character_knowledge", {})
        if not isinstance(existing, dict):
            existing = {}
        deep_merge(existing, character_items)
        normalized["character_knowledge"] = existing

    return normalized or patch


def normalize_state_patch(filename: str, patch: dict[str, Any]) -> dict[str, Any]:
    if filename == "knowledge_state.json":
        return normalize_knowledge_patch(patch)
    container_key = STATE_ITEM_CONTAINER_KEYS.get(filename)
    if container_key:
        return normalize_container_patch(patch, container_key)
    return patch


def write_json_state(session_id: str, filename: str, patch: dict[str, Any]) -> None:
    current = read_json_state(session_id, filename)
    normalized_patch = normalize_state_patch(filename, patch)
    deep_merge(current, normalized_patch)
    current["updated_at"] = utc_now()
    write_state(session_id, filename, current)
'''
    text = replace_once(text, old_state_helpers, new_state_helpers, "JSON/state helpers")

    old_slices = '''def build_relationship_slice(session_id: str, scene_ids: list[str]) -> dict[str, Any]:
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
'''
    new_slices = '''def build_relationship_slice(session_id: str, scene_ids: list[str]) -> dict[str, Any]:
    relationships_state = read_json_state(session_id, "relationships.json")
    relationships = state_container_items(relationships_state, "relationships")
    result: dict[str, Any] = {}
    for key, value in relationships.items():
        participants = relationship_participants(key, value)
        if len([cid for cid in participants if cid in scene_ids]) >= 2:
            result[key] = value
    return result


def build_knowledge_slice(session_id: str, scene_ids: list[str]) -> dict[str, Any]:
    knowledge = read_json_state(session_id, "knowledge_state.json")
    character_knowledge = knowledge.get("character_knowledge", {})
    if not isinstance(character_knowledge, dict):
        character_knowledge = {}

    result: dict[str, Any] = {
        cid: character_knowledge.get(cid, {})
        for cid in scene_ids
        if isinstance(character_knowledge.get(cid, {}), dict)
    }

    speaker_labels = knowledge.get("speaker_labels", {})
    if isinstance(speaker_labels, dict):
        focused_labels = {cid: speaker_labels[cid] for cid in scene_ids if cid in speaker_labels}
        if focused_labels:
            result["_speaker_labels"] = focused_labels

    return result


def build_open_threads_slice(session_id: str, scene_ids: list[str]) -> dict[str, Any]:
    open_threads_state = read_json_state(session_id, "open_threads.json")
    open_threads = state_container_items(open_threads_state, "threads")
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
    incidents_state = read_json_state(session_id, "shared_incidents.json")
    incidents = state_container_items(incidents_state, "incidents")
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
'''
    text = replace_once(text, old_slices, new_slices, "runtime slices")

    old_event_read = '''    event_seeds = read_json_state(session_id, "event_seeds.json")
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
'''
    new_event_read = '''    event_seeds = read_json_state(session_id, "event_seeds.json")
    event_queue = read_json_state(session_id, "event_queue.json")
    director_notes = read_json_state(session_id, "director_notes.json")
    gossip_state = read_json_state(session_id, "gossip_state.json")
    rating_state = read_json_state(session_id, "rating_state.json")
    energy_incidents = read_json_state(session_id, "energy_incidents.json")

    event_seeds_items = state_container_items(event_seeds, "items")
    event_queue_items = state_container_items(event_queue, "items")
    gossip_items = state_container_items(gossip_state, "items")
    energy_incident_items = state_container_items(energy_incidents, "items")
    rating_items = state_container_items(rating_state, "items")

    rating_slice = {
        cid: rating_items.get(cid, {})
        for cid in scene_ids
        if isinstance(rating_items.get(cid, {}), dict)
    }
'''
    text = replace_once(text, old_event_read, new_event_read, "event engine reads")
    text = text.replace('''            event_seeds,
            scene_ids,''', '''            event_seeds_items,
            scene_ids,''', 1)
    text = text.replace('''            event_queue,
            scene_ids,''', '''            event_queue_items,
            scene_ids,''', 1)
    text = text.replace('''            gossip_state,
            scene_ids,''', '''            gossip_items,
            scene_ids,''', 1)
    text = text.replace('''            energy_incidents,
            scene_ids,''', '''            energy_incident_items,
            scene_ids,''', 1)

    old_simple_parse = '''            current_state_changes=parse_json_text(req.current_state_changes_json),
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
'''
    new_simple_parse = '''            current_state_changes=parse_json_text(req.current_state_changes_json, "current_state_changes_json"),
            knowledge_changes=parse_json_text(req.knowledge_changes_json, "knowledge_changes_json"),
            relationship_changes=parse_json_text(req.relationship_changes_json, "relationship_changes_json"),
            open_thread_changes=parse_json_text(req.open_thread_changes_json, "open_thread_changes_json"),
            shared_incident_changes=parse_json_text(req.shared_incident_changes_json, "shared_incident_changes_json"),
            inventory_changes=parse_json_text(req.inventory_changes_json, "inventory_changes_json"),
            character_memory_changes=parse_json_text(req.character_memory_changes_json, "character_memory_changes_json"),
            event_seed_changes=parse_json_text(req.event_seed_changes_json, "event_seed_changes_json"),
            event_queue_changes=parse_json_text(req.event_queue_changes_json, "event_queue_changes_json"),
            director_note_changes=parse_json_text(req.director_note_changes_json, "director_note_changes_json"),
            gossip_changes=parse_json_text(req.gossip_changes_json, "gossip_changes_json"),
            rating_changes=parse_json_text(req.rating_changes_json, "rating_changes_json"),
            energy_incident_changes=parse_json_text(req.energy_incident_changes_json, "energy_incident_changes_json"),
'''
    text = replace_once(text, old_simple_parse, new_simple_parse, "applyTurnResultSimple JSON parsing")

    path.write_text(text, encoding="utf-8")
    print("OK: app/main.py patched")


if __name__ == "__main__":
    root = find_repo_root()
    patch_app_main(root)
    print("Готово. Остальные файлы из ZIP можно просто заменить поверх репозитория.")
