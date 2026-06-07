# Turn Contract Route Decorator Fix

## Problem

`/api/v1/sessions/{session_id}/turn-contract` was accidentally registered on helper function:

```python
@app.post("/api/v1/sessions/{session_id}/turn-contract")
def build_classic_required_files(...)
```

The real `get_turn_contract(...)` function had no decorator, so the Action could not return a usable turn-contract.

## Fix

Decorator moved to:

```python
@app.post("/api/v1/sessions/{session_id}/turn-contract")
def get_turn_contract(session_id: str, req: TurnContractRequest) -> dict[str, Any]:
```

## After upload

1. Commit directly to main.
2. Wait Railway deploy.
3. `/health` should show `3.5.2`.
4. Update Actions schema.
5. Start a fresh chat/session.
