#!/usr/bin/env python3
"""
Apply Academy 1198 v3 runtime patch.

Run from repository root:
    python scripts/apply_v3_runtime_patch.py

This script modifies app/main.py idempotently:
- adds character_slice to scene_contract;
- adds npc_autonomy_contract to scene_contract;
- adds engine/npc_autonomy_rules.md to CORE_REQUIRED_FILES;
- strengthens delayed-character event selection protocol;
- improves header weather/state formatting slightly.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path.cwd()
MAIN = ROOT / "app" / "main.py"


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        fail(f"anchor not found for {label}")
    return text.replace(old, new, 1)


def insert_before(text: str, anchor: str, block: str, label: str) -> str:
    if block.strip() in text:
        return text
    if anchor not in text:
        fail(f"anchor not found for {label}")
    return text.replace(anchor, block.rstrip() + "\n\n" + anchor, 1)


def insert_after(text: str, anchor: str, block: str, label: str) -> str:
    if block.strip() in text:
        return text
    if anchor not in text:
        fail(f"anchor not found for {label}")
    return text.replace(anchor, anchor + "\n" + block.rstrip() + "\n", 1)


def main() -> None:
    if not MAIN.exists():
        fail("app/main.py not found. Run this script from repo root.")

    text = MAIN.read_text(encoding="utf-8")
    original = text

    # 1) Add npc autonomy rules file to CORE_REQUIRED_FILES.
    if '"engine/npc_autonomy_rules.md"' not in text:
        text = replace_once(
            text,
            '    "engine/novel_director_core.md",\n',
            '    "engine/novel_director_core.md",\n    "engine/npc_autonomy_rules.md",\n',
            "CORE_REQUIRED_FILES npc_autonomy_rules",
        )

    # 2) Add build_character_slice before item_related_to_scene.
    character_slice_block = r'''
def build_character_slice(session_id: str, character_ids: list[str]) -> dict[str, Any]:
    """Compact full-character slice for normal play turns.

    This solves the common failure where include_file_contents=false returns only
    character IDs, causing active NPCs to sound like UI guides instead of their
    behavior/voice cards.
    """
    result: dict[str, Any] = {}

    for character_id in character_ids:
        folder = character_folder(character_id)
        if not folder:
            continue

        result[character_id] = {
            "folder": folder,
            "character_card": safe_read_text(
                f"characters/{folder}/character_card.yaml",
                session_id,
                max_chars=2500,
            ),
            "behavior": safe_read_text(
                f"characters/{folder}/behavior.md",
                session_id,
                max_chars=5000,
            ),
            "voice": safe_read_text(
                f"characters/{folder}/voice.md",
                session_id,
                max_chars=3500,
            ),
            "knowledge": safe_read_text(
                f"characters/{folder}/knowledge.yaml",
                session_id,
                max_chars=2500,
            ),
        }

    return result
'''
    text = insert_before(text, "def item_related_to_scene(", character_slice_block, "build_character_slice")

    # 3) Add npc_autonomy_contract before build_scene_contract.
    npc_autonomy_block = r'''
def npc_autonomy_contract() -> dict[str, Any]:
    return {
        "priority": "high",
        "player_controls": [
            "POV character actions",
            "POV character direct speech",
            "POV character attempts and choices",
        ],
        "player_does_not_control": [
            "NPC decisions",
            "NPC emotions",
            "NPC obedience",
            "NPC knowledge",
            "NPC attraction, fear, trust or respect",
            "world/system reactions",
            "rumors, rating and staff conclusions",
        ],
        "rules": [
            "NPCs act from their own goals, character, knowledge, relationships and current pressure.",
            "A player command to an NPC is an attempt, not a guaranteed result.",
            "A player thought is not world knowledge.",
            "Do not make NPCs helpful, understanding or compliant by default.",
            "Do not expose NPC inner thoughts as facts; show intent through visible behavior.",
        ],
        "visible_expression_channels": [
            "action",
            "pause",
            "gaze",
            "distance",
            "tone",
            "mistake",
            "word choice",
            "body reaction",
            "social move",
            "refusal to obey",
        ],
    }
'''
    text = insert_before(text, "def build_scene_contract(", npc_autonomy_block, "npc_autonomy_contract")

    # 4) Add character_slice and npc_autonomy_contract to build_scene_contract return.
    if '"character_slice": build_character_slice(session_id, selected["full"]),' not in text:
        text = replace_once(
            text,
            '        "relationship_slice": build_relationship_slice(session_id, scene_ids),\n',
            '        "character_slice": build_character_slice(session_id, selected["full"]),\n'
            '        "npc_autonomy_contract": npc_autonomy_contract(),\n'
            '        "relationship_slice": build_relationship_slice(session_id, scene_ids),\n',
            "scene_contract character_slice/npc_autonomy",
        )

    # 5) Strengthen event selection protocol.
    delayed_rule = '            "Do not use locked/pending delayed character entries until their trigger_after or requires_story_flag is satisfied.",\n'
    if delayed_rule.strip() not in text:
        text = replace_once(
            text,
            '            "Then choose one suitable queued event or seed if it matches current place, characters and pacing.",\n',
            '            "Then choose one suitable queued event or seed if it matches current place, characters and pacing.",\n'
            + delayed_rule,
            "event_engine delayed selection rule",
        )

    # 6) Add checks returned by turn-contract.
    if "Use scene_contract.character_slice for full active characters" not in text:
        text = replace_once(
            text,
            '            "Use scene_contract first; required_files are support, not the whole project.",\n',
            '            "Use scene_contract first; required_files are support, not the whole project.",\n'
            '            "Use scene_contract.character_slice for full active characters before writing their dialogue.",\n'
            '            "Use npc_autonomy_contract: NPC commands are attempts, not guaranteed outcomes.",\n',
            "turn contract checks",
        )

    # 7) Improve weather formatter to avoid overly technical header.
    old_weather = '''def format_weather_human(weather: Any) -> str:
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
'''
    new_weather = '''def format_weather_human(weather: Any) -> str:
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
        wind_text = str(wind)
        if "ветер" not in wind_text:
            wind_text = f"{wind_text} ветер"
        parts.append(wind_text)
    if precipitation and precipitation not in {"нет", "none", "no"}:
        parts.append(str(precipitation))
    if ground and str(ground) not in {"сухо", "сухая"}:
        parts.append(str(ground))
    return ", ".join(parts)
'''
    if old_weather in text:
        text = text.replace(old_weather, new_weather, 1)

    # 8) Avoid adding "без травм" unless explicitly requested.
    old_no_injuries = '''    elif not pain:
        bits.append("без травм")
'''
    new_no_injuries = '''    elif not pain and status.get("show_no_injuries") is True:
        bits.append("без травм")
'''
    if old_no_injuries in text:
        text = text.replace(old_no_injuries, new_no_injuries, 1)

    if text == original:
        print("No changes needed: app/main.py already appears patched.")
        return

    MAIN.write_text(text, encoding="utf-8")
    print("Patched app/main.py successfully.")


if __name__ == "__main__":
    main()
