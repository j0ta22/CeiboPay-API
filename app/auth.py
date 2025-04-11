import os
import hmac
import hashlib
import json
from urllib.parse import parse_qs

def verify_telegram_data(init_data: str) -> bool:
    """
    Verifica la autenticidad de los datos de inicialización de Telegram.
    
    Args:
        init_data (str): Los datos de inicialización de Telegram
        
    Returns:
        bool: True si los datos son válidos, False en caso contrario
    """
    try:
        # Parsear los datos de inicialización
        parsed_data = parse_qs(init_data)
        
        # Obtener el hash de los datos
        hash_str = parsed_data.get('hash', [''])[0]
        if not hash_str:
            return False
            
        # Obtener el token del bot
        bot_token = os.getenv('BOT_TOKEN')
        if not bot_token:
            return False
            
        # Preparar los datos para la verificación
        data_check = []
        for key, value in parsed_data.items():
            if key != 'hash':
                data_check.append(f"{key}={value[0]}")
        data_check.sort()
        data_check_str = "\n".join(data_check)
        
        # Calcular el hash esperado
        secret_key = hashlib.sha256(bot_token.encode()).digest()
        hmac_obj = hmac.new(secret_key, data_check_str.encode(), hashlib.sha256)
        expected_hash = hmac_obj.hexdigest()
        
        # Comparar los hashes
        return hmac.compare_digest(hash_str, expected_hash)
        
    except Exception as e:
        print(f"Error al verificar datos de Telegram: {str(e)}")
        return False 