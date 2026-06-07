# Balanced Compact Contract Rules

## Problem

`scene_contract_v5_ultra_compact` fixed ResponseTooLargeError but made scenes too short and generic.

## Fix

Use `scene_contract_v5_balanced_compact`.

It is still compact, but preserves enough quality data:

- active character runtime summaries up to useful length;
- focus-reference character summaries for delayed/relevant NPCs;
- richer scene_quality/progress/prose contracts;
- richer event_engine/energy slices;
- active/nearby/mentioned/scheduled/delayed ids in current_state_summary.

## Focus reference rule

If delayed/reference characters are relevant to the beat, include up to 2 as `focus_reference_character_ids`.

They are not automatically active, but GPT can use their runtime summaries if the scene pressure brings them in.

## Goal

No ResponseTooLargeError, but also no short dumb scenes.
