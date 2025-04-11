# app/routes/users.py

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas
from app.database import get_db
from app.dependencies.telegram import verify_telegram_init_data

router = APIRouter(
    prefix="/users",
    tags=["Usuarios"]
)

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
