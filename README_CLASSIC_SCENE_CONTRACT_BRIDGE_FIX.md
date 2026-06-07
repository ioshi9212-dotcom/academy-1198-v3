# Classic Scene Contract Bridge Fix

## What it fixes

After Classic Restore, API 3.5.0 returned `turn_contract_classic_v2`, but `scene_contract` was marked as disabled/backward-compatibility only.

Some GPT/Action gate layers still expected a usable `scene_contract`, so play stopped with the old phrase:

`Не удалось собрать scene assembly packet через Action...`

## Fix

API now returns:

```text
scene_contract.version = scene_contract_classic_bridge_v1
scene_contract.usable = true
```

This bridge mirrors the classic turn-contract data.

## Main contract

The real primary contract remains:

```text
turn_contract_classic_v2
```

The scene_contract bridge only exists so old scene gate checks do not stop play.

## After upload

1. Commit directly to main.
2. Wait for Railway Success.
3. Check `/health`: version should be `3.5.1`.
4. Update Actions schema.
5. Use Custom GPT Instructions from:
   `gpt/custom_gpt_instructions_CLASSIC_RESTORE.md`
