# Academy 1198 v3 — Combined Fix

This package combines:

1. Balanced Compact Quality Fix
   - fixes too-short/dumb scenes caused by ultra compact contract;
   - returns scene_contract_v5_balanced_compact;
   - preserves more scene_quality/progress/prose data;
   - gives focus_reference runtime summaries for relevant delayed/reference NPCs.

2. Calendar 15 Aug Simple Fix
   - simplifies 15 August calendar;
   - keeps Akira energy hidden at start;
   - forbids automatic Akira energy clarification/check on ordinary registration;
   - tells AI to create interesting hooks instead of following rigid registration steps.

Upload everything to GitHub preserving folders.
Commit directly to main.
After Railway deploy, update Actions schema because app/main.py is included.
Then replace Custom GPT Instructions with:
gpt/custom_gpt_instructions_BALANCED_COMPACT.md
