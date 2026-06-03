# Railway Setup

## Volume

Create a Railway Volume and mount it at:

```text
/data
```

Set variables:

```text
PROJECT_SLUG=academy-1198-v3
NOVELLA_RUNTIME_DATA_ROOT=/data
PUBLIC_BASE_URL=https://your-service.up.railway.app
COMPACT_EVERY_TURNS=15
```

## Runtime layout

```text
/data/sessions/{session_id}/state/
```

No active game should use shared `/data/state`.

## Deploy check

Open:

```text
/health
/debug/volume
/openapi-actions.json
```

If `/debug/volume` shows runtime_root under `/data`, persistence is working.
