from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import users, products
import os

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CeiboPay API",
    description="API para la aplicación CeiboPay",
    version="1.0.0"
)

# Configuración CORS
origins = [
    "https://telegram.org",
    "https://web.telegram.org",
    "https://*.telegram.org",
    "https://*.t.me",
    "https://ceibopay-miniapp.netlify.app",
    "http://localhost:5173",  # Para desarrollo local
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Incluir routers
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(products.router, prefix="/products", tags=["products"])

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a CeiboPay API",
        "status": "ok",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Endpoint para verificar el estado del servidor"""
    return {
        "status": "ok",
        "message": "Servidor funcionando correctamente",
        "database_configured": bool(os.getenv("DATABASE_URL")),
        "bot_token_configured": bool(os.getenv("BOT_TOKEN"))
    }
