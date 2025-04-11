from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import schemas
from app.crud import crud

router = APIRouter(prefix="/purchases", tags=["purchases"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.CompraOut)
def create_purchase(compra: schemas.CompraCreate, db: Session = Depends(get_db)):
    return crud.create_purchase(db, compra)

@router.get("/user/{telegram_id}", response_model=list[schemas.CompraOut])
def get_user_purchases(telegram_id: int, db: Session = Depends(get_db)):
    return crud.get_purchases_by_user(db, telegram_id)

@router.get("/seller/{telegram_id}", response_model=list[schemas.CompraOut])
def get_user_sales(telegram_id: int, db: Session = Depends(get_db)):
    return crud.get_sales_by_user(db, telegram_id)

@router.post("/", response_model=schemas.CompraOut)
def create_purchase(purchase: schemas.CompraCreate, db: Session = Depends(get_db)):
    return crud.create_purchase(db, purchase)

@router.get("/{id}", response_model=schemas.CompraOut)
def get_purchase_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_purchase_by_id(db, id)

@router.get("/user/{telegram_id}", response_model=List[schemas.CompraOut])
def get_purchases_by_user(telegram_id: int, db: Session = Depends(get_db)):
    return crud.get_purchases_by_user(db, telegram_id)

@router.get("/sales/{telegram_id}", response_model=List[schemas.CompraOut])
def get_sales_by_user(telegram_id: int, db: Session = Depends(get_db)):
    return crud.get_sales_by_user(db, telegram_id)
