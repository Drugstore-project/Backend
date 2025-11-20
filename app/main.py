from fastapi import FastAPI
from app.database import Base, engine
from app.models import *  # importa models para o create_all
from app.routers import users, products
from app.routers import auth as auth_router
from app.routers import orders
from app.routers import payments
from app.routers import prescriptions
from app.routers import role_router

app = FastAPI(title="Drugstore API (FastAPI)")

# Em dev: cria tabelas automaticamente
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(orders.router)
app.include_router(payments.router)
app.include_router(prescriptions.router, prefix="/prescriptions", tags=["Prescriptions"])
app.include_router(role_router.router)

