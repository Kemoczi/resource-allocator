import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app, get_db
from app.database import Base
from app.init_db import resources
from app.models import Resource


TEST_DB_URL = "sqlite:///./test_db.db"

engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    session = TestingSessionLocal()

    try:
        session.query(Resource).delete()
        session.commit()

        session.add_all(Resource(**resource) for resource in resources)
        session.commit()

        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def test_client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def create_payload():
    def _create_payload(location=None, phy_speed=None, optics=None):
        payload = {}
        if location is not None:
            payload["location"] = location
        if phy_speed is not None:
            payload["phy_speed"] = phy_speed
        if optics is not None:
            payload["optics"] = optics
        return payload

    return _create_payload
