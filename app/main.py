from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Literal

from fastapi import FastAPI, HTTPException
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

app = FastAPI(title=f"{PROJECT_SLUG} GPT Actions API", version="3.0.0")

class CreateSessionRequest(BaseModel):
    session_id: str | None = None
    reset: bool = True

class TurnContractRequest(BaseModel):
    user_input: str
    mode: Literal["play", "technical", "audit", "transfer"] = "play"
    include_file_contents: bool = True

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

class CompactRequest(BaseModel):
    reason: str = "scheduled_compaction"
    compact_last_turns: int = 15
    recent_turns_md: str | None = None
    state_updates: dict[str, Any] = Field(default_factory=dict)


def trim(text: str) -> dict[str, Any]:
    if len(text) <= MAX_FILE_CHARS:
        return {"content": text, "truncated": False, "chars": len(text)}
    return {"content": text[:MAX_FILE_CHARS], "truncated": True, "chars": len(text)}


def deep_merge(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            base[key] = deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def read_json_state(session_id: str, filename: str) -> dict[str, Any]:
    value = read_state(session_id, filename)
    return value if isinstance(value, dict) else {}


def write_json_state(session_id: str, filename: str, patch: dict[str, Any]) -> None:
    current = read_json_state(session_id, filename)
    deep_merge(current, patch)
    current["updated_at"] = utc_now()
    write_state(session_id, filename, current)


def build_required_files(current_state: dict[str, Any], mode: str) -> list[str]:
    base = [
        "MANCHESS_RULES.md",
        "engine/turn_contract.md",
        "engine/loading_policy.md",
        "engine/source_priority.md",
        "engine/scene_generation_rules.md",
        "engine/output_format.md",
        "engine/pov_rules.md",
        "engine/npc_knowledge_rules.md",
        "engine/memory_update_rules.md",
        "engine/anti_hallucination_rules.md",
        "story/pacing/no_filler_rules.md",
        "validation/checklist_before_scene.md",
        "validation/calendar_skip_check.md",
        "state/current_state.json",
        "state/recent_turns.md",
    ]
    month = str(current_state.get("current_date", "1206-08-31"))[:7]
    if month:
        base.append(f"story/calendar/{month}.yaml")
    arc_id = current_state.get("current_arc_id")
    if isinstance(arc_id, str) and arc_id:
        base.append(f"story/arcs/{arc_id}.yaml")
    return list(dict.fromkeys(base))


@app.on_event("startup")
def startup() -> None:
    ensure_runtime_root()

@app.get("/")
def root() -> dict[str, Any]:
    return {"status": "ok", "project": PROJECT_SLUG, "actions_schema": "/openapi-actions.json"}

@app.get("/health")
def health() -> dict[str, Any]:
    return {"success": True, "project": PROJECT_SLUG, "time": utc_now()}

@app.get("/debug/volume")
def debug_volume() -> dict[str, Any]:
    return {"success": True, **debug_info()}

@app.post("/api/v1/sessions")
def create_session(req: CreateSessionRequest) -> dict[str, Any]:
    sid, root = ensure_session(req.session_id, reset=req.reset)
    return {
        "success": True,
        "session_id": sid,
        "session_root": str(root),
        "state_root": str(session_state_root(sid)),
        "next": {"turn_contract": f"/api/v1/sessions/{sid}/turn-contract"},
    }

@app.post("/api/v1/sessions/{session_id}/turn-contract")
def get_turn_contract(session_id: str, req: TurnContractRequest) -> dict[str, Any]:
    sid, _ = ensure_session(session_id, reset=False)
    current_state = read_json_state(sid, "current_state.json")
    required_files = build_required_files(current_state, req.mode)
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
        "required_files": required_files,
        "required_file_contents": contents,
        "checks": [
            "Use current session runtime state, not old chat memory.",
            "Load active characters by ID only.",
            "NPCs speak from their own knowledge, not hidden canon.",
            "After a meaningful scene, call applyTurnResult.",
        ],
    }

@app.post("/api/v1/sessions/{session_id}/apply-turn-result")
def apply_turn_result(session_id: str, req: ApplyTurnResultRequest) -> dict[str, Any]:
    sid, root = ensure_session(session_id, reset=False)
    state_root = session_state_root(sid)
    if req.technical:
        append_jsonl(root / "technical_history.jsonl", {"time": utc_now(), "scene_id": req.scene_id, "text": req.scene_text})
        return {"success": True, "status": "technical_saved", "session_id": sid}

    append_jsonl(state_root / "scene_history.jsonl", {"time": utc_now(), "scene_id": req.scene_id, "scene_text": req.scene_text})

    patch_map = [
        ("current_state.json", req.current_state_changes),
        ("knowledge_state.json", req.knowledge_changes),
        ("relationships.json", req.relationship_changes),
        ("open_threads.json", req.open_thread_changes),
        ("shared_incidents.json", req.shared_incident_changes),
        ("inventory_state.json", req.inventory_changes),
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
    compaction["compact_every_turns"] = int(compaction.get("compact_every_turns", COMPACT_EVERY_TURNS) or COMPACT_EVERY_TURNS)
    compaction["needs_compaction"] = compaction["since_last_compaction"] >= compaction["compact_every_turns"]
    compaction["last_scene_id"] = req.scene_id
    compaction["updated_at"] = utc_now()
    write_state(sid, "compaction_state.json", compaction)
    updated.append("compaction_state.json")

    return {"success": True, "session_id": sid, "updated_files": updated, "needs_compaction": compaction.get("needs_compaction", False)}

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

@app.get("/api/v1/files/{file_path:path}")
def read_file(file_path: str, session_id: str | None = None) -> PlainTextResponse:
    try:
        text = read_project_or_runtime_file(safe_repo_path(file_path), session_id)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return PlainTextResponse(text)

@app.get("/openapi-actions.json")
def openapi_actions() -> dict[str, Any]:
    server = PUBLIC_BASE_URL or "https://your-service.up.railway.app"
    return {
        "openapi": "3.1.0",
        "info": {"title": f"{PROJECT_SLUG} GPT Actions", "version": "3.0.0"},
        "servers": [{"url": server}],
        "paths": {
            "/health": {"get": {"operationId": "healthCheck", "summary": "Check API health", "responses": {"200": {"description": "OK"}}}},
            "/debug/volume": {"get": {"operationId": "debugVolume", "summary": "Check runtime volume", "responses": {"200": {"description": "OK"}}}},
            "/api/v1/sessions": {"post": {"operationId": "createSession", "summary": "Create a new runtime session", "requestBody": {"required": False, "content": {"application/json": {"schema": CreateSessionRequest.model_json_schema()}}}, "responses": {"200": {"description": "Session created"}}}},
            "/api/v1/sessions/{session_id}/turn-contract": {"post": {"operationId": "getSessionTurnContract", "summary": "Get files and runtime state for one turn", "parameters": [{"name": "session_id", "in": "path", "required": True, "schema": {"type": "string"}}], "requestBody": {"required": True, "content": {"application/json": {"schema": TurnContractRequest.model_json_schema()}}}, "responses": {"200": {"description": "Turn contract"}}}},
            "/api/v1/sessions/{session_id}/apply-turn-result": {"post": {"operationId": "applyTurnResult", "summary": "Persist scene and state changes", "parameters": [{"name": "session_id", "in": "path", "required": True, "schema": {"type": "string"}}], "requestBody": {"required": True, "content": {"application/json": {"schema": ApplyTurnResultRequest.model_json_schema()}}}, "responses": {"200": {"description": "Saved"}}}},
            "/api/v1/sessions/{session_id}/compact": {"post": {"operationId": "compactSessionMemory", "summary": "Persist memory compaction", "parameters": [{"name": "session_id", "in": "path", "required": True, "schema": {"type": "string"}}], "requestBody": {"required": True, "content": {"application/json": {"schema": CompactRequest.model_json_schema()}}}, "responses": {"200": {"description": "Compacted"}}}},
        },
    }
