from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ----------- PRODUCTO -----------

class ProductoBase(BaseModel):
    nombre: str
    descripcion: str
    precio: float


class ProductoCreate(ProductoBase):
    usuario_id: int


class ProductoOut(ProductoBase):
    id: int
    nombre: str
    descripcion: str
    precio: float
    created_at: datetime

    class Config:
        from_attributes = True

# ----------- USUARIO -----------

class UsuarioBase(BaseModel):
    telegram_id: str
    username: Optional[str] = None
    location: Optional[str] = None
    wallet: Optional[str] = None
    public_key: Optional[str] = None
    encrypted_private_key: Optional[str] = None


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioOut(UsuarioBase):
    telegram_id: int
    username: Optional[str]
    wallet: Optional[str]
    productos: List[ProductoOut] = []

    class Config:
        from_attributes = True


class WalletUpdate(BaseModel):
    wallet: str

# ----------- COMPRA -----------

class CompraBase(BaseModel):
    producto_id: int
    comprador_id: int
    vendedor_id: int


class CompraCreate(CompraBase):
    pass


class CompraOut(CompraBase):
    id: int
    fecha: datetime

    class Config:
        from_attributes = True

