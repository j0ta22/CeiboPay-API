from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas
from datetime import datetime


def create_user(db: Session, user: schemas.UsuarioCreate):
    db_user = models.Usuario(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_telegram_id(db: Session, telegram_id: str):
    return db.query(models.Usuario).filter(models.Usuario.telegram_id == telegram_id).first()

def create_product(db: Session, product: schemas.ProductoCreate):
    db_product = models.Producto(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_all_products(db: Session):
    return db.query(models.Producto).all()

def get_products_by_user(db: Session, telegram_id: int):
    return db.query(models.Producto).filter(models.Producto.usuario_id == telegram_id).all()

def update_product(db: Session, product_id: int, product_data: schemas.ProductoCreate):
    product = db.query(models.Producto).filter(models.Producto.id == product_id).first()
    if not product:
        return None  # O lanzar HTTPException(status_code=404)

    product.nombre = product_data.nombre
    product.descripcion = product_data.descripcion
    product.precio = product_data.precio
    product.usuario_id = product_data.usuario_id

    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int):
    product = db.query(models.Producto).filter(models.Producto.id == product_id).first()
    if not product:
        return None  # o lanzar excepción
    db.delete(product)
    db.commit()
    return product


def create_purchase(db: Session, compra: schemas.CompraCreate):
    # Validar que el producto existe
    producto = db.query(models.Producto).filter(models.Producto.id == compra.producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Validar que el vendedor sea el dueño del producto
    if producto.usuario_id != compra.vendedor_id:
        raise HTTPException(status_code=400, detail="El vendedor no coincide con el dueño del producto")

    # Crear compra
    db_compra = models.Compra(
        producto_id=compra.producto_id,
        comprador_id=compra.comprador_id,
        vendedor_id=compra.vendedor_id,
        precio_pagado=producto.precio  # Agregamos el precio pagado desde el producto
    )
    db.add(db_compra)
    db.commit()
    db.refresh(db_compra)
    return db_compra

def get_purchases_by_user(db: Session, telegram_id: int):
    return db.query(models.Compra).filter(models.Compra.comprador_id == telegram_id).all()

def get_sales_by_user(db: Session, telegram_id: int):
    return db.query(models.Compra).filter(models.Compra.vendedor_id == telegram_id).all()

def create_purchase(db: Session, compra: schemas.CompraCreate):
    db_compra = models.Compra(
        producto_id=compra.producto_id,
        comprador_id=compra.comprador_id,
        vendedor_id=compra.vendedor_id,
        created_at=datetime.utcnow()
    )
    db.add(db_compra)
    db.commit()
    db.refresh(db_compra)
    return db_compra

def get_purchase_by_id(db: Session, compra_id: int):
    return db.query(models.Compra).filter(models.Compra.id == compra_id).first()

def get_purchases_by_user(db: Session, telegram_id: int):
    return db.query(models.Compra).filter(models.Compra.comprador_id == telegram_id).all()

def get_sales_by_user(db: Session, telegram_id: int):
    return db.query(models.Compra).filter(models.Compra.vendedor_id == telegram_id).all()



