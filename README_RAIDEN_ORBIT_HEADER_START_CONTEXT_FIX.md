# Raiden/Haru/Kiara Orbit + Header/Start Context Fix

## Version

API: `3.5.9`

## Includes

Based on the previous full package:
- Akira v2 default;
- Akira social mask;
- academy uniform visuals.

## Fixes

### Header format

Restores strict play-scene wrapper:

```text
━━━━━━━━━━━━━━━━━━━━
📅 ...
🕒 ...
📍 ...
🌤 ...
🫀 ...
🎒 ...
━━━━━━━━━━━━━━━━━━━━
```

Ending block is also wrapped in separator lines.

### Akira start context

At the start Akira has:

```text
чёрная рубашка, бордовый пиджак Академии, чёрная юбка-шорты, ботинки, сумка с одеждой, документы, телефон
```

### Haru / Raiden / Kiara orbit

Strengthened:
- Haru and Raiden often appear together or in the same public/social/training zone.
- If one enters a public/social/training scene, the other should often be nearby/reference unless state gives a reason absent.
- Kiara often keeps near their social orbit, especially in public/status/flirt/rivalry scenes.
- Kiara is not always present and her interest is not automatically romantic.

## After upload

1. Upload ZIP to GitHub.
2. Commit directly to `main`.
3. Wait Railway deploy.
4. `/health` should show `3.5.9`.
5. Update Actions schema:
   `https://web-production-cd472.up.railway.app/openapi-actions.json`
6. Start a new session.
