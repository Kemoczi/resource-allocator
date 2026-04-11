import pytest
import requests


@pytest.mark.testclient
class TestWithClient:

    def test_wrong_query(self, test_client, create_payload):
        payload = create_payload(location="Olesnica", phy_speed="10G", optics="10GBASE-SR")

        response = test_client.post("/resources/assign-interface", json=payload)
        data = response.json()

        assert response.status_code == 404
        assert data == {"detail": "No resources with specified parameters available"}

    def test_empty_query(self, test_client, create_payload):
        payload = create_payload()

        response = test_client.post("/resources/assign-interface", json=payload)
        data = response.json()

        assert response.status_code == 400
        assert data == {"detail": "You must provide at least one resource parameter"}


@pytest.mark.live
class TestLiveServer:

    def test_wrong_query_live(self, live_server, create_payload, check_time):
        payload = create_payload(location="Olesnica", phy_speed="10G", optics="10GBASE-SR")

        with check_time():
            response = requests.post(f"{live_server}/resources/assign-interface", json=payload, timeout=3)
        data = response.json()

        assert response.status_code == 404
        assert data == {"detail": "No resources with specified parameters available"}

    def test_empty_query_live(self, live_server, create_payload, check_time):
        payload = create_payload()

        with check_time():
            response = requests.post(f"{live_server}/resources/assign-interface", json=payload, timeout=3)
        data = response.json()

        assert response.status_code == 400
        assert data == {"detail": "You must provide at least one resource parameter"}
