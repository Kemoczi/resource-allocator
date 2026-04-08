import requests
import sys
import subprocess
import pytest
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

@pytest.fixture(scope="module")
def live_server():
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
    )

    base_url = "http://127.0.0.1:8001"

    try:
        for _ in range(30):
            try:
                response = requests.get(f"{base_url}/", timeout=0.5)
                if response.status_code == 200:
                    break
            except requests.RequestException:
                time.sleep(0.2)
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

def test_root_live(live_server):
    response = requests.get(f"{live_server}/", timeout=2)

    assert response.status_code == 200
    assert response.json() == {"message": "Hello, this is resource allocator! ;)"}





def test_resources(live_server):
    response = requests.get(f"{live_server}/resources/", timeout=2)
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 10