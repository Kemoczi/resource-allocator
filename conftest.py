import pytest
import subprocess
import sys
import os
import requests
from pathlib import Path
from time import sleep
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app, get_db
from app.database import Base
from app.init_db import resources
from app.models import Resource
from app.free_resources import free_resources


TEST_DB_URL = "sqlite:///./test_db.db"


@pytest.fixture(scope="module")
def testing_db_session():
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
    session = TestingSessionLocal()

    try:
        session.query(Resource).delete()
        session.commit()

        session.add_all(Resource(**resource) for resource in resources)
        session.commit()

        yield session
    finally:
        session.close()


@pytest.fixture(scope="module")
def test_client(testing_db_session):
    def override_get_db():
        yield testing_db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope="module")
def live_server():
    env = os.environ.copy()
    env["DATABASE_URL"] = "sqlite:///./test_uvicorn.db"
    PROJECT_ROOT = Path(__file__).resolve().parent

    subprocess.run(
        [sys.executable, "-m", "app.init_db"],
        cwd=PROJECT_ROOT,
        env=env,
        check=True,
    )

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8001",
        ],
        cwd=PROJECT_ROOT,
        env=env
    )

    base_url = "http://127.0.0.1:8001"

    try:
        for _ in range(10):
            try:
                response = requests.get(f"{base_url}/", timeout=0.5)
                if response.status_code == 200:
                    break
            except requests.RequestException:
                sleep(0.2)
        else:
            stdout, stderr = process.communicate(timeout=1)
            raise RuntimeError(
                f"Uvicorn did not start in time.\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}"
            )
        yield base_url

    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        free_resources()



@pytest.fixture
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
