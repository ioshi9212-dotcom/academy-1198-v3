# Files safe to delete after Classic Restore

These are old patch artifacts or cache files. They are not used by `turn_contract_classic_v2`.

Delete if they exist in GitHub:

```text
README_BALANCED_COMPACT_QUALITY_FIX.md
README_CALENDAR_15AUG_SIMPLE_FIX.md
README_COMBINED_FIX.md
README_FORMAT_AUG31_FIX.md
README_VOICE_FIT_GATE_FIX.md
engine/ultra_compact_contract_rules.md
engine/balanced_compact_contract_rules.md
gpt/custom_gpt_instructions_BALANCED_COMPACT.md
gpt/custom_gpt_instructions_FORMAT_PATCH.md
gpt/custom_gpt_instructions_VOICE_FIT_PATCH.md
validation/balanced_compact_quality_checklist.md
app/__pycache__/main.cpython-313.pyc
```

Notes:
- ZIP upload to GitHub does not delete files that are absent from the ZIP.
- If these old files remain, they should not affect runtime, because `app/main.py` now uses `turn_contract_classic_v2`.
- Keeping them is mostly clutter, not a gameplay bug.
