from fastapi import FastAPI
from app.database import Base, engine
from app.routes import users, products

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(products.router)

@app.get("/")
def root():
    return {"message": "CeiboPay API funcionando 👋"}
