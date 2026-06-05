from __future__ import annotations

import json
import os
import shutil
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STATE_TEMPLATE_DIRNAME = "state_templates"
STATE_DIRNAME = "state"

STATE_FILES = [
    "current_state.json",
    "knowledge_state.json",
    "relationships.json",
    "shared_incidents.json",
    "open_threads.json",
    "inventory_state.json",
    "compaction_state.json",
    "recent_turns.md",
    "event_seeds.json",
    "event_queue.json",
    "director_notes.json",
    "gossip_state.json",
    "rating_state.json",
    "energy_incidents.json",
]

RUNTIME_DIRS = ["sessions", "logs", "backups", "exports", "tmp"]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def runtime_root() -> Path:
    root = (
        os.getenv("NOVELLA_RUNTIME_DATA_ROOT")
        or os.getenv("RAILWAY_VOLUME_MOUNT_PATH")
        or str(project_root() / "runtime_data")
    )
    return Path(root).expanduser().resolve()


@dataclass(frozen=True)
class StoragePaths:
    project_root: Path
    runtime_root: Path
    sessions_root: Path
    logs_root: Path
    backups_root: Path
    exports_root: Path
    tmp_root: Path
    templates_root: Path


def paths() -> StoragePaths:
    root = project_root()
    rr = runtime_root()
    return StoragePaths(
        project_root=root,
        runtime_root=rr,
        sessions_root=rr / "sessions",
        logs_root=rr / "logs",
        backups_root=rr / "backups",
        exports_root=rr / "exports",
        tmp_root=rr / "tmp",
        templates_root=root / STATE_TEMPLATE_DIRNAME,
    )


def ensure_runtime_root() -> StoragePaths:
    p = paths()
    for name in RUNTIME_DIRS:
        (p.runtime_root / name).mkdir(parents=True, exist_ok=True)
    p.templates_root.mkdir(parents=True, exist_ok=True)
    return p


def safe_session_id(session_id: str | None = None) -> str:
    if not session_id:
        return "session_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_") + uuid.uuid4().hex[:6]
    safe = "".join(ch for ch in session_id if ch.isalnum() or ch in "-_")
    return safe or safe_session_id(None)


def session_root(session_id: str) -> Path:
    p = ensure_runtime_root()
    root = p.sessions_root / safe_session_id(session_id)
    root.mkdir(parents=True, exist_ok=True)
    return root


def session_state_root(session_id: str) -> Path:
    root = session_root(session_id) / STATE_DIRNAME
    root.mkdir(parents=True, exist_ok=True)
    return root


def copy_template_file(src: Path, dst: Path, session_id: str, reset: bool = False) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and not reset:
        return
    if src.exists():
        text = src.read_text(encoding="utf-8")
        text = text.replace("{{SESSION_ID}}", session_id)
        text = text.replace("{{CREATED_AT}}", utc_now())
        dst.write_text(text, encoding="utf-8")
    else:
        dst.write_text("{}\n" if dst.suffix == ".json" else "", encoding="utf-8")


def ensure_session(session_id: str | None = None, reset: bool = False) -> tuple[str, Path]:
    sid = safe_session_id(session_id)
    p = paths()
    state_root = session_state_root(sid)
    for filename in STATE_FILES:
        copy_template_file(p.templates_root / filename, state_root / filename, sid, reset)
    (state_root / "character_memory").mkdir(parents=True, exist_ok=True)
    marker = state_root / "character_memory" / ".gitkeep"
    if not marker.exists():
        marker.write_text("", encoding="utf-8")
    return sid, session_root(sid)


def read_text(path: Path, default: str = "") -> str:
    if not path.exists():
        return default
    return path.read_text(encoding="utf-8")


def read_json(path: Path, default: Any) -> Any:
    raw = read_text(path).strip()
    if not raw:
        return default
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return default


def write_json_atomic(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def append_jsonl(path: Path, item: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")


def read_state(session_id: str, filename: str) -> Any:
    ensure_session(session_id)
    path = session_state_root(session_id) / filename
    if filename.endswith(".md"):
        return read_text(path)
    return read_json(path, {} if filename != "scene_history.jsonl" else [])


def write_state(session_id: str, filename: str, data: Any) -> None:
    ensure_session(session_id)
    path = session_state_root(session_id) / filename
    if filename.endswith(".md") and isinstance(data, str):
        path.write_text(data, encoding="utf-8")
    else:
        write_json_atomic(path, data)


def safe_repo_path(raw_path: str) -> str:
    normalized = raw_path.replace("\\", "/").strip().lstrip("/")
    parts = [p for p in normalized.split("/") if p]
    if not parts or any(p == ".." for p in parts):
        raise ValueError("Unsafe path")
    return "/".join(parts)


def read_project_or_runtime_file(file_path: str, session_id: str | None = None) -> str:
    safe = safe_repo_path(file_path)
    if session_id and safe.startswith("state/"):
        candidate = session_state_root(session_id) / Path(safe).name
        if candidate.exists():
            return read_text(candidate)
    path = project_root() / safe
    return read_text(path)


def debug_info() -> dict[str, str]:
    p = ensure_runtime_root()
    return {
        "project_root": str(p.project_root),
        "runtime_root": str(p.runtime_root),
        "sessions_root": str(p.sessions_root),
        "templates_root": str(p.templates_root),
    }
