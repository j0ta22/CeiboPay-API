from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import users, products
import os

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configurar CORS
allowed_origins = [
    "https://ceibopay.netlify.app",  # Frontend en producción
    "http://localhost:5173",         # Frontend en desarrollo
    "https://ceibopay-miniapp.netlify.app",  # MiniApp en producción
    "https://web.telegram.org",      # Telegram Web
    "https://t.me"                   # Telegram
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(users.router)
app.include_router(products.router)

@app.get("/")
def root():
    return {"message": "CeiboPay API funcionando 👋"}
