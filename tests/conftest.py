import os
import pytest
import tempfile
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Connection
from app.db.base import Base
from app.main import app
from app import database as app_database
from app.database import get_db
from fastapi.testclient import TestClient


@pytest.fixture(scope="session", autouse=True)
def test_sqlite_db(tmp_path_factory):
    """
    Create a fresh sqlite file for the whole test session and remove it afterwards.
    Also override app.database.engine and SessionLocal so application code uses this DB.
    """
    tmpdir = tmp_path_factory.mktemp("testdbs")
    db_path = tmpdir / "test.db"
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # override the app's database globals so imported modules use the test engine/session
    app_database.engine = engine
    app_database.SessionLocal = TestingSessionLocal

    # create schema
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield engine, TestingSessionLocal, db_path

    # teardown: drop tables, dispose engine and remove file
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    try:
        os.remove(str(db_path))
    except FileNotFoundError:
        pass


@pytest.fixture()
def db(test_sqlite_db):
    """
    Per-test transactional session: begin a transaction on a connection and rollback at the end.
    This gives each test isolation while keeping schema creation fast (session-scoped).
    """
    engine, TestingSessionLocal, _ = test_sqlite_db

    connection: Connection = engine.connect()
    transaction = connection.begin()

    # bind a session to the connection
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def client(test_sqlite_db):
    """
    TestClient that uses the testing session for dependency injection.
    Overrides the FastAPI get_db dependency so endpoints use the same test DB.
    """
    _, TestingSessionLocal, _ = test_sqlite_db

    def _get_test_db():
        db_session = TestingSessionLocal()
        try:
            yield db_session
        finally:
            db_session.close()

    # override dependency
    app.dependency_overrides[get_db] = _get_test_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
