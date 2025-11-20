"""
Main application entry point.
Configures FastAPI app, routes, and database initialization.
"""
from fastapi import FastAPI
from app.database import Base, engine
# Import models to ensure they are registered with Base.metadata
# pylint: disable=unused-import
from app import models
from app.routers import (
    users,
    products,
    auth as auth_router,
    orders,
    payments,
    prescriptions,
    role_router,
    reports
)

app = FastAPI(title="Drugstore API (FastAPI)")

# Em dev: cria tabelas automaticamente
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    """
    Health check endpoint.
    """
    return {"status": "ok"}

app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(orders.router)
app.include_router(payments.router)
app.include_router(prescriptions.router, prefix="/prescriptions", tags=["Prescriptions"])
app.include_router(role_router.router)
app.include_router(reports.router)

