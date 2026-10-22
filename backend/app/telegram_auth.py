import os
import hmac
import hashlib
from urllib.parse import parse_qsl, urlparse
from itsdangerous import URLSafeSerializer

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Telegram initData verification per https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app

def _check_signature(init_data: str) -> dict:
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not set")
    # init_data is querystring-like
    pairs = dict(parse_qsl(init_data, keep_blank_values=True))
    hash_ = pairs.pop("hash", None)
    if not hash_:
        raise ValueError("Missing hash")
    # Construct data-check-string
    data_check = "\n".join(f"{k}={pairs[k]}" for k in sorted(pairs.keys()))
    secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
    calc_hash = hmac.new(secret_key, data_check.encode(), hashlib.sha256).hexdigest()
    if calc_hash != hash_:
        raise ValueError("Invalid initData hash")
    return pairs


def verify_init_data(init_data: str):
    pairs = _check_signature(init_data)
    # user is JSON string in pairs['user']
    import json
    user = json.loads(pairs.get("user", "{}"))
    start_param = pairs.get("start_param")
    return {"id": user.get("id"), "first_name": user.get("first_name"), "start_param": start_param}
