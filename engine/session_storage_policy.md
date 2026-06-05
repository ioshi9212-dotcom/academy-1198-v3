# Session Storage Policy

## Roles

GitHub stores:

- canon;
- engine rules;
- templates;
- starter files;
- API code;
- validation files.

Railway Volume stores:

- live sessions;
- runtime state;
- scene history;
- character memory;
- relationships;
- open threads;
- compacted memory;
- logs;
- backups.

GPT Actions/API connects the current chat to the correct Railway session.

## Runtime session path

Every live game session uses:

```text
/data/sessions/{session_id}/state/
```

A new game creates a new `session_id`.

The API copies `state_templates/` into that session state folder.

## Session rules

- A new game must not silently reuse an old game session.
- `session_id` belongs to the current chat.
- `apply-turn-result` writes only to the active session.
- `compact` works only inside the active session.
- GitHub state templates are not live memory.
- Live memory is not written back into GitHub unless explicitly exported as canon or transfer notes.

## Debug

A default/debug session may exist for development.

It must not be used as the normal game session when a fresh game starts.
