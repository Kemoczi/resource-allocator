import requests
import pytest

# TODO: Maupa ze sleepem zeby strzelil timeout

@pytest.mark.live
def test_root_live(live_server):
    response = requests.get(f"{live_server}/", timeout=2)

    assert response.status_code == 200
    assert response.json() == {"message": "Hello, this is resource allocator! ;)"}




@pytest.mark.live
def test_resources(live_server):
    response = requests.get(f"{live_server}/resources/", timeout=2)
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 10