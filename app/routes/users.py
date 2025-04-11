# app/routes/users.py

from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas
from app.database import get_db
from app.dependencies.telegram import verify_telegram_init_data
import os
from sqlalchemy import text
import datetime
from typing import List
from ..auth import verify_telegram_data

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/sync")
async def sync_user(request: Request, db: Session = Depends(get_db)):
    """Endpoint para sincronizar usuarios desde el bot"""
    try:
        data = await request.json()
        telegram_id = data.get("telegram_id")
        username = data.get("username")
        wallet = data.get("wallet")
        
        if not all([telegram_id, wallet]):
            raise HTTPException(status_code=400, detail="Faltan datos requeridos")
            
        # Verificar si el usuario existe
        user = db.query(models.Usuario).filter_by(telegram_id=telegram_id).first()
        
        if user:
            # Actualizar usuario existente
            user.wallet = wallet
            if username:
                user.username = username
        else:
            # Crear nuevo usuario
            user = models.Usuario(
                telegram_id=telegram_id,
                username=username,
                wallet=wallet
            )
            db.add(user)
            
        db.commit()
        return {"status": "success", "message": "Usuario sincronizado correctamente"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/db-check")
def verificar_db(db: Session = Depends(get_db)):
    """Endpoint para verificar la conexión a la base de datos y listar usuarios"""
    try:
        # Verificar conexión
        db.execute(text("SELECT 1"))
        
        # Consulta SQL directa para usuarios
        result = db.execute(text("""
            SELECT telegram_id, username, wallet, created_at
            FROM usuarios
            ORDER BY created_at DESC
        """))
        
        usuarios = []
        for row in result:
            usuarios.append({
                "telegram_id": row[0],
                "username": row[1],
                "wallet": row[2],
                "created_at": row[3].isoformat() if row[3] else None
            })
            
        # Obtener información de la base de datos
        db_info = db.execute(text("""
            SELECT current_database(), current_user, version()
        """)).first()
            
        return {
            "status": "success",
            "total_usuarios": len(usuarios),
            "usuarios": usuarios,
            "database_info": {
                "name": db_info[0],
                "user": db_info[1],
                "version": db_info[2]
            },
            "database_url": os.getenv("DATABASE_URL", ""),
            "bot_token_configured": bool(os.getenv("BOT_TOKEN")),
            "environment": os.getenv("ENVIRONMENT", "production")
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "database_url": os.getenv("DATABASE_URL", ""),
            "bot_token_configured": bool(os.getenv("BOT_TOKEN")),
            "environment": os.getenv("ENVIRONMENT", "production")
        }

@router.get("/debug")
async def debug_telegram(request: Request, db: Session = Depends(get_db)):
    """Endpoint para depurar los datos de Telegram"""
    headers = dict(request.headers)
    
    # Verificar si hay usuarios en la base de datos
    total_usuarios = db.query(models.Usuario).count()
    
    return {
        "headers": headers,
        "bot_token_configured": bool(os.getenv("BOT_TOKEN")),
        "init_data": headers.get("x-telegram-init-data"),
        "total_usuarios": total_usuarios,
        "usuarios": [
            {
                "telegram_id": u.telegram_id,
                "username": u.username,
                "wallet": u.wallet
            } for u in db.query(models.Usuario).all()
        ]
    }

@router.get("/all")
def listar_usuarios(db: Session = Depends(get_db)):
    """Endpoint para listar todos los usuarios"""
    usuarios = db.query(models.Usuario).all()
    return {
        "total_usuarios": len(usuarios),
        "usuarios": [
            {
                "telegram_id": u.telegram_id,
                "username": u.username,
                "wallet": u.wallet
            } for u in usuarios
        ]
    }

@router.get("/telegram/{telegram_id}")
async def get_user_by_telegram_id(
    telegram_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """Obtener usuario por ID de Telegram"""
    # Verificar datos de Telegram
    init_data = request.headers.get("X-Telegram-Init-Data")
    if not init_data or not verify_telegram_data(init_data):
        raise HTTPException(status_code=401, detail="No autorizado")

    # Buscar usuario en la base de datos
    user = db.query(models.Usuario).filter(models.Usuario.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user

@router.put("/{telegram_id}/wallet")
async def update_wallet(
    telegram_id: int,
    wallet_data: schemas.WalletUpdate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Actualizar wallet de usuario"""
    # Verificar datos de Telegram
    init_data = request.headers.get("X-Telegram-Init-Data")
    if not init_data or not verify_telegram_data(init_data):
        raise HTTPException(status_code=401, detail="No autorizado")

    # Buscar usuario
    user = db.query(models.Usuario).filter(models.Usuario.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Actualizar wallet
    user.wallet = wallet_data.wallet
    if wallet_data.encrypted_private_key:
        user.encrypted_private_key = wallet_data.encrypted_private_key

    db.commit()
    db.refresh(user)
    return user

@router.put("/bot/{telegram_id}/wallet")
async def actualizar_wallet_bot(
    telegram_id: int,
    wallet_data: schemas.WalletUpdate,
    x_bot_token: str = Header(None),
    db: Session = Depends(get_db)
):
    """Actualizar la wallet desde el bot"""
    # Verificar el token del bot
    if not x_bot_token or x_bot_token != os.getenv("BOT_TOKEN"):
        raise HTTPException(status_code=403, detail="Token de bot inválido")
    
    # Buscar el usuario
    user = db.query(models.Usuario).filter(models.Usuario.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Actualizar la wallet
    user.wallet = wallet_data.wallet
    if wallet_data.encrypted_private_key:
        user.encrypted_private_key = wallet_data.encrypted_private_key
    
    db.commit()
    db.refresh(user)
    
    return user

@router.get("/health")
async def health_check():
    """Endpoint para verificar el estado del servidor"""
    return {
        "status": "ok",
        "message": "Servidor funcionando correctamente",
        "timestamp": datetime.datetime.now().isoformat(),
        "database_configured": bool(os.getenv("DATABASE_URL")),
        "bot_token_configured": bool(os.getenv("BOT_TOKEN"))
    }
