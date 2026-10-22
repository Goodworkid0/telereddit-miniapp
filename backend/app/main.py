import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from .telegram_auth import verify_init_data
from .webhook import router as webhook_router

load_dotenv()

app = FastAPI(title="TeleReddit API")

# CORS for Vite dev
origins = ["http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static serving (for production build)
WEB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../webapp/dist"))
if os.path.isdir(WEB_DIR):
    app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="static")

@app.post("/api/session/verify")
async def session_verify(payload: dict):
    init_data = payload.get("initData", "")
    try:
        user = verify_init_data(init_data)
        return {"ok": True, "user": user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/health")
async def health():
    return {"ok": True}

# Telegram webhook endpoints
app.include_router(webhook_router, prefix="/api")
