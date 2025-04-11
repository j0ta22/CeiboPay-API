# app/routes/users.py

from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas
from app.database import get_db
from app.dependencies.telegram import verify_telegram_init_data
import os
from sqlalchemy import text

router = APIRouter(
    prefix="/users",
    tags=["Usuarios"]
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
            SELECT telegram_id, username, wallet 
            FROM usuarios
        """))
        
        usuarios = []
        for row in result:
            usuarios.append({
                "telegram_id": row[0],
                "username": row[1],
                "wallet": row[2]
            })
            
        return {
            "status": "success",
            "total_usuarios": len(usuarios),
            "usuarios": usuarios
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@router.get("/debug")
async def debug_telegram(request: Request):
    """Endpoint para depurar los datos de Telegram"""
    headers = dict(request.headers)
    return {
        "headers": headers,
        "bot_token_configured": bool(os.getenv("BOT_TOKEN")),
        "init_data": headers.get("x-telegram-init-data"),
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

@router.get("/telegram/{telegram_id}", response_model=schemas.UsuarioOut)
def obtener_usuario_telegram(
    telegram_id: int,
    init_data: str = Header(..., alias="X-Telegram-Init-Data"),
    db: Session = Depends(get_db)
):
    if not verify_telegram_init_data(init_data):
        raise HTTPException(status_code=403, detail="Init data inválido")

    user = db.query(models.Usuario).filter_by(telegram_id=telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return user

@router.put("/{telegram_id}/wallet", response_model=schemas.UsuarioOut)
def actualizar_wallet(
    telegram_id: int,
    wallet_data: schemas.WalletUpdate,
    init_data: str = Header(..., alias="X-Telegram-Init-Data"),
    db: Session = Depends(get_db)
):
    if not verify_telegram_init_data(init_data):
        raise HTTPException(status_code=403, detail="Init data inválido")

    user = db.query(models.Usuario).filter_by(telegram_id=telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user.wallet = wallet_data.wallet
    db.commit()
    db.refresh(user)
    
    return user
