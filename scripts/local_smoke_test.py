from __future__ import annotations

import json
import os
import shutil
import tempfile
from typing import Any

from fastapi import HTTPException


def fail(message: str) -> None:
    raise AssertionError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def require_dict(value: Any, path: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"{path} must be dict, got {type(value).__name__}")
    return value


def require_text(value: Any, path: str, min_len: int = 40) -> str:
    require(isinstance(value, str), f"{path} must be str, got {type(value).__name__}")
    require(len(value.strip()) >= min_len, f"{path} is too short or empty")
    return value


def json_text(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False)


def main() -> None:
    temp_root = tempfile.mkdtemp(prefix="academy_1198_v3_ci_")
    os.environ["NOVELLA_RUNTIME_DATA_ROOT"] = temp_root
    os.environ.setdefault("PROJECT_SLUG", "academy-1198-v3")

    try:
        from app.main import (  # noqa: WPS433 - local smoke test imports app directly
            ApplyTurnResultSimpleRequest,
            CreateSessionRequest,
            TurnContractRequest,
            apply_turn_result_simple,
            create_session,
            get_turn_contract,
            read_json_state,
        )

        session = create_session(CreateSessionRequest(session_id="ci_premerge_runtime", reset=True))
        require(session.get("success") is True, "create_session did not return success=True")
        session_id = str(session.get("session_id"))
        require(session_id, "session_id missing")

        contract = get_turn_contract(
            session_id,
            TurnContractRequest(
                user_input="CI pre-merge runtime check: start scene contract",
                mode="play",
                include_file_contents=False,
            ),
        )
        require(contract.get("success") is True, "get_turn_contract did not return success=True")
        require(contract.get("is_game_turn") is True, "play turn must be marked is_game_turn=True")

        current_state = require_dict(contract.get("current_state"), "current_state")
        require(current_state.get("current_date") == "1198-08-15", "start date must be 1198-08-15")
        require(current_state.get("current_arc_id") == "arc_001_academy_start", "wrong start arc")
        require(current_state.get("current_location_id") == "loc_academy_main", "wrong start location")

        active_ids = current_state.get("active_character_ids")
        require(isinstance(active_ids, list), "active_character_ids must be list")
        require("char_akira" in active_ids, "char_akira must be active at start")
        require("char_livia" in active_ids, "char_livia must be active at start")

        scene_contract = require_dict(contract.get("scene_contract"), "scene_contract")

        # Required runtime slices. These are the main anti-regression checks.
        for key in [
            "current_frame",
            "calendar_slice",
            "arc_slice",
            "location_slice",
            "character_load_plan",
            "character_slice",
            "character_memory_slice",
            "npc_autonomy_contract",
            "relationship_behavior_contract",
            "knowledge_write_contract",
            "memory_write_contract",
            "relationship_slice",
            "knowledge_slice",
            "open_threads_slice",
            "shared_incidents_slice",
            "event_engine_slice",
            "response_format_contract",
            "scene_density_contract",
        ]:
            require(key in scene_contract, f"scene_contract missing required key: {key}")

        character_slice = require_dict(scene_contract.get("character_slice"), "scene_contract.character_slice")
        for cid in ["char_akira", "char_livia"]:
            cdata = require_dict(character_slice.get(cid), f"character_slice.{cid}")
            require_text(cdata.get("behavior"), f"character_slice.{cid}.behavior", min_len=120)
            require_text(cdata.get("voice"), f"character_slice.{cid}.voice", min_len=120)
            require_text(cdata.get("character_card"), f"character_slice.{cid}.character_card", min_len=40)

        livia_blob = json.dumps(character_slice.get("char_livia", {}), ensure_ascii=False).lower()
        require("гид" in livia_blob or "guide" in livia_blob, "Livia behavior must explicitly protect against guide-mode")
        require("акира" in livia_blob, "Livia slice must include her connection to Akira")

        npc_contract = require_dict(scene_contract.get("npc_autonomy_contract"), "npc_autonomy_contract")
        require("player_does_not_control" in npc_contract or "rules" in npc_contract, "npc_autonomy_contract is too weak")

        memory_contract = require_dict(scene_contract.get("memory_write_contract"), "memory_write_contract")
        memory_dump = json.dumps(memory_contract, ensure_ascii=False).lower()
        require("spoken" in memory_dump or "фраз" in memory_dump, "memory_write_contract must mention important spoken lines")
        require("relationship" in memory_dump or "отнош" in memory_dump, "memory_write_contract must mention relationships")
        require("knowledge" in memory_dump or "знан" in memory_dump, "memory_write_contract must mention knowledge")

        rel_contract = require_dict(scene_contract.get("relationship_behavior_contract"), "relationship_behavior_contract")
        rel_dump = json.dumps(rel_contract, ensure_ascii=False).lower()
        for token in ["trust", "tension", "respect"]:
            require(token in rel_dump, f"relationship_behavior_contract must use {token}")

        relationship_slice = require_dict(scene_contract.get("relationship_slice"), "relationship_slice")
        rel_akira_livia = relationship_slice.get("char_akira__char_livia") or relationship_slice.get("char_livia__char_akira")
        require(isinstance(rel_akira_livia, dict), "start relationship char_akira__char_livia must be seeded")
        require("behavior_next" in rel_akira_livia, "Akira/Livia relationship must include behavior_next")

        knowledge_slice = require_dict(scene_contract.get("knowledge_slice"), "knowledge_slice")
        require("char_livia" in knowledge_slice, "knowledge_slice must include char_livia start knowledge")

        # Persist a meaningful scene result and verify the runtime reads it back next turn.
        apply_result = apply_turn_result_simple(
            session_id,
            ApplyTurnResultSimpleRequest(
                scene_id="ci_runtime_scene_001",
                scene_text=(
                    "CI scene: Akira gave a controlled minimal energy response; "
                    "Livia heard it and reacted in her own voice."
                ),
                current_state_changes_json=json_text(
                    {
                        "current_scene_id": "ci_runtime_scene_001",
                        "story_flags": {"ci_first_entry_pressure_shown": True},
                    }
                ),
                knowledge_changes_json=json_text(
                    {
                        "character_knowledge": {
                            "char_livia": {
                                "seen_events": [
                                    {
                                        "scene_id": "ci_runtime_scene_001",
                                        "summary": "Ливия видела, что Акира прошла проверку минимальным откликом.",
                                        "certainty": "seen_directly",
                                    }
                                ],
                                "beliefs": [
                                    {
                                        "fact_id": "akira_controls_energy_quietly_ci",
                                        "text": "Акира умеет пройти проверку тихо, не раскрывая лишнего.",
                                        "certainty": "medium",
                                        "source": "ci_runtime_scene_001",
                                    }
                                ],
                            }
                        },
                        "evidence_log": [
                            {
                                "scene_id": "ci_runtime_scene_001",
                                "fact": "Controlled minimal energy response was observed.",
                                "visible_to": ["char_livia"],
                            }
                        ],
                    }
                ),
                relationship_changes_json=json_text(
                    {
                        "relationships": {
                            "char_akira__char_livia": {
                                "characters": ["char_akira", "char_livia"],
                                "trust": 76,
                                "tension": 12,
                                "respect": 48,
                                "curiosity": 12,
                                "memory": [
                                    {
                                        "scene_id": "ci_runtime_scene_001",
                                        "summary": "Акира ответила Ливии спокойно перед проверкой; Ливия не должна превращаться в гид.",
                                        "importance": "important",
                                    }
                                ],
                                "behavior_next": "Ливия может шутить и прикрывать напряжение, но реагирует на спокойствие Акиры и не говорит за неё.",
                                "last_interaction": "ci_runtime_scene_001",
                            }
                        }
                    }
                ),
                shared_incident_changes_json=json_text(
                    {
                        "incidents": {
                            "incident_ci_minimal_energy_check": {
                                "date": "1198-08-15",
                                "time": "08:45",
                                "location_id": "loc_academy_main",
                                "participants": ["char_akira", "char_livia"],
                                "witnesses": ["char_livia"],
                                "visible_facts": [
                                    "Акира прошла входную проверку минимальным энергетическим откликом.",
                                    "Ливия была рядом и слышала короткую реплику Акиры.",
                                ],
                                "spoken_lines": [
                                    {
                                        "speaker": "char_akira",
                                        "line": "ожидаемо, не паникуй.",
                                        "importance": "important",
                                        "reason": "Фраза влияет на тон близкой связки Акиры и Ливии.",
                                    }
                                ],
                                "relationship_changes": ["char_akira__char_livia"],
                                "status": "active_reference",
                            }
                        }
                    }
                ),
                character_memory_changes_json=json_text(
                    {
                        "char_livia": {
                            "seen_events": [
                                {
                                    "date": "1198-08-15",
                                    "time": "08:45",
                                    "scene_id": "ci_runtime_scene_001",
                                    "incident_id": "incident_ci_minimal_energy_check",
                                    "summary": "Акира прошла проверку спокойно и удержала отклик минимальным.",
                                    "certainty": "seen_directly",
                                }
                            ],
                            "heard_events": [
                                {
                                    "date": "1198-08-15",
                                    "time": "08:45",
                                    "scene_id": "ci_runtime_scene_001",
                                    "incident_id": "incident_ci_minimal_energy_check",
                                    "summary": "Акира сказала: ожидаемо, не паникуй.",
                                    "certainty": "heard_directly",
                                }
                            ],
                            "relationships_from_this_character": {
                                "char_akira": {
                                    "trust": 76,
                                    "tension": 12,
                                    "respect": 48,
                                    "private_status": "старая близкая подруга; Ливия шумит, но знает привычки Акиры",
                                    "behavior_next": "Отвечать живо и своим голосом, не становиться справочником Академии.",
                                }
                            },
                        }
                    }
                ),
            ),
        )
        require(apply_result.get("success") is True, "apply_turn_result_simple did not return success=True")

        relationships_state = read_json_state(session_id, "relationships.json")
        rels = require_dict(relationships_state.get("relationships"), "relationships.json.relationships")
        require("char_akira__char_livia" in rels, "relationship patch was not saved under relationships container")
        require(rels["char_akira__char_livia"].get("trust") == 76, "relationship trust did not persist")

        incidents_state = read_json_state(session_id, "shared_incidents.json")
        incidents = require_dict(incidents_state.get("incidents"), "shared_incidents.json.incidents")
        require("incident_ci_minimal_energy_check" in incidents, "shared incident was not saved")
        require(incidents["incident_ci_minimal_energy_check"].get("spoken_lines"), "important spoken line was not saved")

        contract_after = get_turn_contract(
            session_id,
            TurnContractRequest(
                user_input="CI pre-merge runtime check: verify memory loaded back",
                mode="play",
                include_file_contents=False,
            ),
        )
        scene_after = require_dict(contract_after.get("scene_contract"), "scene_contract after save")

        memory_slice = require_dict(scene_after.get("character_memory_slice"), "character_memory_slice after save")
        require("char_livia" in memory_slice, "character_memory_slice must load char_livia memory after save")
        livia_memory_dump = json.dumps(memory_slice["char_livia"], ensure_ascii=False)
        require("ожидаемо, не паникуй" in livia_memory_dump, "important Akira line must be visible in Livia memory next turn")

        rel_after = require_dict(scene_after.get("relationship_slice"), "relationship_slice after save")
        rel_after_data = rel_after.get("char_akira__char_livia") or rel_after.get("char_livia__char_akira")
        require(isinstance(rel_after_data, dict), "relationship must load back into next turn contract")
        require("behavior_next" in rel_after_data, "relationship behavior_next must load back into next turn")

        # Bad JSON must fail loudly. Silent {} would hide broken memory saves.
        try:
            apply_turn_result_simple(
                session_id,
                ApplyTurnResultSimpleRequest(
                    scene_id="ci_bad_json",
                    current_state_changes_json="{bad json",
                ),
            )
        except HTTPException as exc:
            require(exc.status_code == 400, "bad JSON must return HTTP 400")
        else:
            fail("bad JSON was accepted silently")

        print("✅ academy-1198-v3 runtime smoke test passed")

    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


if __name__ == "__main__":
    main()
