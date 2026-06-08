# Academy Uniform Visual Fix

## Version

API: `3.5.8`

## Purpose

Adds academy uniform visual rules into existing runtime/contract files, without creating a separate uniform lock.

## Rules added

Base academy uniform:
- dark burgundy blazer/jacket;
- dark shirt;
- gold academy details;
- for girls: skirt is standard, tie/ribbon/neck detail optional, practical shoes.

Variation rule:
- not everyone follows the ideal form;
- some wear white instead of dark shirt;
- skirts can be shorter/longer;
- students may add jewelry, belts, pins;
- sleeves may be rolled;
- shirts may be untucked;
- tie may be removed;
- this reflects character/image/status, not official ideal.

Akira:
- burgundy blazer with gold emblem/details;
- black shirt;
- black skirt-shorts instead of standard skirt;
- no tie;
- long heavy black boots;
- very long loose white hair.

## Files changed

- `app/main.py`
- `runtime/academy/energy_atmosphere.yaml`
- `runtime/characters/akira_v2.yaml`
- `state_templates/current_state.json`

## After upload

1. Commit directly to main.
2. Wait Railway deploy.
3. Check `/health`: should show `3.5.8`.
4. Update Actions schema.
5. Start a new session.
