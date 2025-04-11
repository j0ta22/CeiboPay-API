from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, BigInteger, func
from sqlalchemy.orm import relationship
from app.database import Base  # Asegurate que este es tu declarative_base

class Usuario(Base):
    __tablename__ = "usuarios"

    telegram_id = Column(BigInteger, primary_key=True, index=True)  # Es el ID único del bot
    username = Column(String, index=True, nullable=True)
    location = Column(String, nullable=True)
    wallet = Column(String, nullable=True)
    public_key = Column(String, nullable=True)
    encrypted_private_key = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    productos = relationship("Producto", back_populates="usuario", cascade="all, delete")
    compras_realizadas = relationship("Compra", foreign_keys="Compra.comprador_id", back_populates="comprador")
    ventas_realizadas = relationship("Compra", foreign_keys="Compra.vendedor_id", back_populates="vendedor")


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    usuario_id = Column(BigInteger, ForeignKey("usuarios.telegram_id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    usuario = relationship("Usuario", back_populates="productos")
    compras = relationship("Compra", back_populates="producto", cascade="all, delete")


class Compra(Base):
    __tablename__ = "compras"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    comprador_id = Column(BigInteger, ForeignKey("usuarios.telegram_id"), nullable=False)
    vendedor_id = Column(BigInteger, ForeignKey("usuarios.telegram_id"), nullable=False)
    precio_pagado = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    producto = relationship("Producto", back_populates="compras")
    comprador = relationship("Usuario", foreign_keys=[comprador_id], back_populates="compras_realizadas")
    vendedor = relationship("Usuario", foreign_keys=[vendedor_id], back_populates="ventas_realizadas")
