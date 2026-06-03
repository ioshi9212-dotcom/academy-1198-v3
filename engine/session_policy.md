# ManChess Session Policy

1. At the beginning of every new ChatGPT chat, create a new session.
2. Never reuse a session_id from memory, previous chat, docs, examples, or tests.
3. Store session_id only inside the current chat context.
4. If no session_id exists in the current chat, call createSession.
5. Test sessions are disposable and must not become canon gameplay sessions.
6. Old sessions can only be resumed if user explicitly provides session_id and asks to continue it.
