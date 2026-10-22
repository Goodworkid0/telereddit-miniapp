import os
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import CommandStart
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL") or "http://localhost:5173"
BOT_USERNAME = os.getenv("BOT_USERNAME", "")

router = Router()

def parse_slug(start_text: str | None) -> str:
    if not start_text:
        return "general"
    parts = start_text.split(" ", 1)
    start_param = parts[1] if len(parts) > 1 else None
    slug = (start_param.split(":", 1)[1] if start_param and ":" in start_param else start_param)
    return slug or "general"

@router.message(CommandStart())
async def start(message: Message):
    slug = parse_slug(message.text)

    buttons = []
    # Mini App button (opens inside Telegram)
    buttons.append([InlineKeyboardButton(text="Open community", web_app=WebAppInfo(url=f"{WEB_APP_URL}?startapp=community:{slug}"))])

    # Deep link via t.me if username configured
    if BOT_USERNAME:
        deep_link = f"https://t.me/{BOT_USERNAME}/app?startapp=community:{slug}"
        buttons.append([InlineKeyboardButton(text="Open via t.me", url=deep_link)])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(f"Welcome to TeleReddit! Opening community: {slug}", reply_markup=kb)


def get_dispatcher():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN not set")
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    return bot, dp
