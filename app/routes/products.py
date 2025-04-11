from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import crud
from app.schemas import schemas
from app.database import SessionLocal

router = APIRouter(prefix="/products", tags=["products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.ProductoOut)
def create(product: schemas.ProductoCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@router.get("/", response_model=list[schemas.ProductoOut])
def get_all(db: Session = Depends(get_db)):
    return crud.get_all_products(db)

@router.get("/user/{telegram_id}", response_model=list[schemas.ProductoOut])
def get_by_user(telegram_id: int, db: Session = Depends(get_db)):
    return crud.get_products_by_user(db, telegram_id)

@router.put("/{product_id}", response_model=schemas.ProductoOut)
def update_product(product_id: int, updated_product: schemas.ProductoCreate, db: Session = Depends(get_db)):
    return crud.update_product(db, product_id, updated_product)


@router.delete("/{product_id}", response_model=schemas.ProductoOut)
def delete(product_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return deleted

