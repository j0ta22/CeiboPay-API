import hashlib
import hmac
import urllib.parse
import os

def verify_telegram_init_data(init_data: str) -> bool:
    """Verifica la firma de Telegram usando el token del bot"""
    bot_token = os.getenv("BOT_TOKEN")
    secret_key = hashlib.sha256(bot_token.encode()).digest()

    parsed = urllib.parse.parse_qs(init_data)
    data_check_string = "\n".join(
        f"{k}={v[0]}" for k, v in sorted(parsed.items()) if k != "hash"
    )
    received_hash = parsed.get("hash", [None])[0]
    
    if not received_hash:
        return False

    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    return hmac.compare_digest(calculated_hash, received_hash)
