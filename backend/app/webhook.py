import os
from fastapi import APIRouter, Request, HTTPException, status
from aiogram.types import Update
from .bot import get_dispatcher

router = APIRouter()

# Lazy init to avoid crashing the app when BOT_TOKEN is missing during local dev
bot = None
dp = None

def ensure_dispatcher():
    global bot, dp
    if bot is None or dp is None:
        bot, dp = get_dispatcher()

@router.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    try:
        ensure_dispatcher()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
    try:
        data = await request.json()
        update = Update.model_validate(data)
        await dp.feed_webhook_update(bot, update)
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
