# TeleReddit Backend

Run locally:

1. Create `.env` from `.env.example` and set BOT_TOKEN, APP_BASE_URL
2. Install deps (already configured via workspace tools)
3. Start API server:

```
poetry run python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The webapp dev server runs on http://localhost:5173; configure CORS or proxy later if needed.
