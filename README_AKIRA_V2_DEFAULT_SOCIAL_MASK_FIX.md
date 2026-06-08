# Akira v2 Default + Social Mask Fix

## Version

API: `3.5.7`

## Includes previous not-yet-uploaded fix

This ZIP includes the v2 default fix:
- Akira default runtime is `version_2_poisonous`.
- `version_1_cold` remains in files as legacy/cold backup.
- fresh sessions start with v2 in `state_templates/current_state.json`.

## New improvement

Akira v2 now has a player-controlled social mask.

She can pretend to be weaker, softer, more obedient, more interested or more frightened than she really is when the player chooses that line.

This is not real helplessness. It is a controlled tactic to make another person relax, overreach, reveal intent or show a weak spot.

## Origin

Akira used to be genuinely quieter/softer. It did not help.

After the Kai/school-past line, she learned that true quietness can make a person an easy target.

The current poisonous mask comes from:
`I was truly quiet. It did not help.`

## Livia

Livia knows Akira can do this and may recognize warning signs:
- too-calm smile;
- too-sweet tone;
- sudden “okay/fine”;
- giving up too early;
- letting someone believe they already won.

## Files changed

- `runtime/characters/akira_v2.yaml`
- `runtime/characters/livia.yaml`
- `gpt/locks/akira_v2_social_mask_lock.md`
- `gpt/locks/akira_v2_default_lock.md`
- `state_templates/current_state.json`
- `runtime/characters/characters_runtime_index.yaml`
- `app/main.py`
- `.github/workflows/classic-runtime-smoke.yml`

## After upload

1. Commit directly to main.
2. Wait Railway deploy.
3. Check `/health`: should show `3.5.7`.
4. Update Actions schema.
5. Start a new session.

Note: `state_templates/current_state.json` is included so fresh sessions start with Akira v2.
