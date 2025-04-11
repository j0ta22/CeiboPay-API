from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import users, products
import os

Base.metadata.create_all(bind=engine)

app = FastAPI()

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

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(products.router, prefix="/products", tags=["products"])

@app.get("/")
async def root():
    return {"message": "Bienvenido a CeiboPay API"}
