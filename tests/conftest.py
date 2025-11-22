import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Connection
from app.db.base import Base
from app.main import app
from app import database as app_database
from app.database import get_db
from fastapi.testclient import TestClient


import os

# CONFIGURAÇÃO DO BANCO DE TESTE
# Tenta usar localhost se não estiver no docker (assumindo que 'db' é para docker)
db_host = os.getenv("DB_HOST", "localhost")
TEST_DATABASE_URL = f"postgresql://druguser:drugpass@{db_host}:5432/drugstore"



@pytest.fixture(scope="session", autouse=True)
def test_postgres_db():
    """
    Usa um banco PostgreSQL REAL para testes.
    Cria e remove todas as tabelas apenas 1 vez por sessão.
    """
    engine = create_engine(TEST_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # override globais da aplicação
    app_database.engine = engine
    app_database.SessionLocal = TestingSessionLocal

    # prepara o schema
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield engine, TestingSessionLocal

    # limpa após toda a suíte de testes
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture()
def db(test_postgres_db):
    """
    Cada teste roda dentro da sua própria transação,
    que é revertida no final.
    """
    engine, TestingSessionLocal = test_postgres_db

    connection: Connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def client(db):
    """
    TestClient usando a mesma sessão `db` para garantir dados consistentes.
    """
    def _get_test_db():
        yield db

    app.dependency_overrides[get_db] = _get_test_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
