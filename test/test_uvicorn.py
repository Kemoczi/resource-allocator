import requests
import pytest


@pytest.mark.live
class TestLiveServer:

    def test_root_live(self, live_server, check_time):
        with check_time():
            response = requests.get(f"{live_server}/", timeout=3)

        assert response.status_code == 200
        assert response.json() == {"message": "Hello, this is resource allocator! ;)"}


    def test_resources(self, live_server, check_time):
        with check_time():
            response = requests.get(f"{live_server}/resources/", timeout=3)
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 10
