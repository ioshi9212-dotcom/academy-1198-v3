# Academy 1198 v3 — Dialogue Format + Aug 31 Energy Privacy Fix

## What it fixes

1. Dialogue/description Markdown format:
   - descriptions/actions/system reactions are separate italic paragraphs;
   - dialogue is `**Name/descriptor** — Reply. (*short note*)`;
   - no colon after speaker;
   - no plain description paragraphs;
   - bottom options/thoughts use POV first person for inner stance.

2. Contract technical bug:
   - balanced compact contract was cutting exact `engine/output_format.md` rules;
   - `response_format_contract` now includes exact body format.

3. Calendar 31 August:
   - no public advertising/classification of student energy types;
   - includes Akira;
   - energy stays visible by consequence, not public exposition.

## Upload

Upload all files preserving folders. Commit directly to main.

Because `app/main.py` changes, after Railway deploy update Actions schema:
https://web-production-cd472.up.railway.app/openapi-actions.json

Custom GPT Instructions can remain the balanced compact version, but if format still drifts, add:
`Use response_format_contract body_format exactly: **Name** — Reply. (*note*); descriptions italic paragraphs.`
