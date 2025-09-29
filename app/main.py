from fastapi import FastAPI
from app.database import Base, engine
from app.models import *  # importa models para o create_all
from app.routers import users, products

app = FastAPI(title="Drugstore API (FastAPI)")

# Cria tabelas no primeiro start (para dev). Em prod, prefira Alembic.
Base.metadata.create_all(bind=engine)

# Healthcheck simples
@app.get("/health")
def health():
    return {"status": "ok"}

# Rotas
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(products.router, prefix="/products", tags=["Products"])
