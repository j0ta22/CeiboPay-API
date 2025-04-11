import hashlib
import hmac
import urllib.parse
import os

def verify_telegram_init_data(init_data: str) -> bool:
    """Verifica la firma de Telegram usando el token del bot"""
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        print("Error: BOT_TOKEN no está configurado en el entorno")
        return False

    print("Bot token encontrado")
    secret_key = hashlib.sha256(bot_token.encode()).digest()

    parsed = urllib.parse.parse_qs(init_data)
    print("Datos parseados:", parsed)
    
    data_check_string = "\n".join(
        f"{k}={v[0]}" for k, v in sorted(parsed.items()) if k != "hash"
    )
    print("Data check string:", data_check_string)
    
    received_hash = parsed.get("hash", [None])[0]
    print("Hash recibido:", received_hash)
    
    if not received_hash:
        print("Error: No se recibió hash en los datos")
        return False

    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    print("Hash calculado:", calculated_hash)

    return hmac.compare_digest(calculated_hash, received_hash)
