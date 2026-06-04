from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("NOVELLA_RUNTIME_DATA_ROOT", str(Path(__file__).resolve().parents[1] / "runtime_data"))

from app.main import (  # noqa: E402
    ApplyTurnResultRequest,
    CreateSessionRequest,
    TurnContractRequest,
    apply_turn_result,
    create_session,
    get_turn_contract,
)


def main() -> None:
    created = create_session(CreateSessionRequest(reset=True))
    session_id = created["session_id"]
    print("SESSION", session_id)
    print("STATE_ROOT", created["state_root"])

    contract = get_turn_contract(
        session_id,
        TurnContractRequest(user_input="начнем", mode="play", include_file_contents=False),
    )
    assert contract["success"] is True
    assert contract["session_id"] == session_id
    assert "state/current_state.json" in contract["required_files"]
    assert "story/calendar/academy_start.yaml" in contract["required_files"]
    assert "story/arcs/arc_001_academy_start.yaml" in contract["required_files"]
    assert "story/calendar/1206-08.yaml" not in contract["required_files"]
    assert "story/arcs/arc_001_start.yaml" not in contract["required_files"]
    print("TURN_CONTRACT_OK", len(contract["required_files"]), "files")

    result = apply_turn_result(
        session_id,
        ApplyTurnResultRequest(
            scene_id="smoke_scene_001",
            scene_text="Smoke test scene text.",
            current_state_changes={
                "current_scene_id": "smoke_scene_001",
                "current_time": "00:01",
            },
            relationship_changes={
                "relationships": {
                    "char_akira__char_livia": {
                        "characters": ["char_akira", "char_livia"],
                        "trust": 0,
                        "tension": 0,
                        "behavior_next": "Smoke test only."
                    }
                }
            },
            character_memory_changes={
                "char_livia": {
                    "seen_events": [
                        {
                            "day_id": "academy_day_001",
                            "time": "00:01",
                            "scene_id": "smoke_scene_001",
                            "summary": "Smoke test event.",
                            "certainty": "seen_directly"
                        }
                    ]
                }
            },
        ),
    )
    assert result["success"] is True
    assert "current_state.json" in result["updated_files"]
    assert "relationships.json" in result["updated_files"]
    assert "character_memory/char_livia.json" in result["updated_files"]
    print("APPLY_RESULT_OK", result["updated_files"])
    print("NEEDS_COMPACTION", result["needs_compaction"])


if __name__ == "__main__":
    main()
