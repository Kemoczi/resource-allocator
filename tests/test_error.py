import pytest
import requests


NON_MATCHING_PAYLOADS = [
    {"location": "Olesnica"},
    {"phy_speed": "2137G"},
    {"phy_speed": "100G", "optics": "1GBASE-SR"},
    {"location": "Zbuczyn", "phy_speed": "0G", "optics": "0GBASE"}
]

INVALID_FILTER_PAYLOADS = [
    {"speed": "10G"},
    {"location": "London", "speed": "10G"},
    {"lo": "London", "speed": "10G", "optic": "100GBASE-LR"}
]


@pytest.mark.testclient
class TestWithClient:

    @pytest.mark.parametrize("payload", NON_MATCHING_PAYLOADS)
    def test_unmatched_payload_returns_404(self, test_client, payload):
        response = test_client.post("/resources/assign-interface", json=payload)
        data = response.json()

        assert response.status_code == 404
        assert data == {"detail": "No resources with specified parameters available"}

    @pytest.mark.parametrize("payload", INVALID_FILTER_PAYLOADS)
    def test_invalid_filter_payload_returns_422(self, test_client, payload):
        response = test_client.post("/resources/assign-interface", json=payload)
        data = response.json()

        assert response.status_code == 422
        assert data == {"detail": "Error - Invalid request body. Check field names."}

    def test_empty_payload_returns_400(self, test_client):
        response = test_client.post("/resources/assign-interface", json={})
        data = response.json()

        assert response.status_code == 400
        assert data == {"detail": "You must provide at least one resource parameter"}


@pytest.mark.live
class TestLiveServer:

    @pytest.mark.parametrize("payload", NON_MATCHING_PAYLOADS)
    def test_unmatched_payload_returns_404_live(self, live_server, payload, check_time):
        with check_time():
            response = requests.post(
                f"{live_server}/resources/assign-interface", json=payload, timeout=3
            )
        data = response.json()

        assert response.status_code == 404
        assert data == {"detail": "No resources with specified parameters available"}

    @pytest.mark.parametrize("payload", INVALID_FILTER_PAYLOADS)
    def test_invalid_filter_payload_returns_422_live(self, live_server, payload, check_time):
        with check_time():
            response = requests.post(
                f"{live_server}/resources/assign-interface", json=payload, timeout=3
            )
        data = response.json()

        assert response.status_code == 422
        assert data == {"detail": "Error - Invalid request body. Check field names."}

    def test_empty_payload_returns_400_live(self, live_server, check_time):
        with check_time():
            response = requests.post(
                f"{live_server}/resources/assign-interface", json={}, timeout=3
            )
        data = response.json()

        assert response.status_code == 400
        assert data == {"detail": "You must provide at least one resource parameter"}
