from __future__ import annotations

from pathlib import Path

REQUIRED_SNIPPETS = {
    "app/main.py": [
        "STATE_ITEM_CONTAINER_KEYS",
        "state_container_items",
        "normalize_state_patch",
        "parse_json_text(req.current_state_changes_json, \"current_state_changes_json\")",
        "relationships = state_container_items(relationships_state, \"relationships\")",
        "character_knowledge = knowledge.get(\"character_knowledge\", {})",
        "open_threads = state_container_items(open_threads_state, \"threads\")",
        "incidents = state_container_items(incidents_state, \"incidents\")",
        "event_seeds_items = state_container_items(event_seeds, \"items\")",
    ],
    "engine/source_priority.md": ["Latest explicit user correction", "Runtime session state"],
    "characters/raiden/behavior.md": ["Gets colder, not louder"],
    "state_templates/event_seeds.json": ["\"items\": {", "seed_white_hair_first_attention"],
    "state_templates/event_queue.json": ["\"items\": {", "event_start_white_hair_attention"],
}


def main() -> None:
    root = Path.cwd()
    missing = []
    for rel, snippets in REQUIRED_SNIPPETS.items():
        path = root / rel
        if not path.exists():
            missing.append(f"missing file: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet not in text:
                missing.append(f"missing snippet in {rel}: {snippet}")
    if missing:
        print("FAILED")
        for item in missing:
            print("-", item)
        raise SystemExit(1)
    print("OK: academy-1198-v3 fixes are present")


if __name__ == "__main__":
    main()
