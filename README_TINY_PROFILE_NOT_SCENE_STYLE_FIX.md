# Tiny Profile Is Not Scene Style Fix

## Problem

The model interpreted `response_profile: tiny_3_5_3` as a prose instruction:
- shorter scene;
- exactly 3 actions / 3 speech lines / 3 thoughts;
- more rigid structure.

That is wrong.

`tiny` is only an API payload profile to avoid ResponseTooLargeError.

## Fix

API version: `3.5.5`

Changes:
- response_profile renamed to `api_payload_tiny_3_5_5_not_scene_style`;
- added `scene_style_contract`;
- added `gpt/locks/tiny_profile_not_scene_style_lock.md`;
- ending blocks now allow 2-4 options, not exactly three.

## Expected behavior

The response remains compact enough for Actions, but the scene itself should not become short/stub-like.

## After upload

1. Commit directly to main.
2. Wait Railway deploy.
3. `/health` should show `3.5.5`.
4. Update Actions schema.
5. Start a fresh session.
