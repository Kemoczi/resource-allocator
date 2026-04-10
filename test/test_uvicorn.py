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


    def test_assign_if_by_speed_live(self, live_server, create_payload, check_time):
        payload = create_payload(phy_speed="100G")

        with check_time():
            response = requests.post(f"{live_server}/resources/assign-interface", json=payload)
        data = response.json()

        assert response.status_code == 200
        assert data["phy_speed"] == "100G"
        assert data["assigned"] is True


    def test_assign_if_by_speed_location_live(self, live_server, create_payload, check_time):
        payload = create_payload(location="London", phy_speed="100G")

        with check_time():
            response = requests.post(f"{live_server}/resources/assign-interface", json=payload)
        data = response.json()

        assert response.status_code == 200
        assert data["phy_speed"] == "100G"
        assert data["location"] == "London"
        assert data["optics"] == "100GBASE-LR"
        assert data["assigned"] is True


    def test_assign_if_by_speed_location_optics_live(self, live_server, create_payload, check_time):
        payload = create_payload(location="London", phy_speed="1G", optics="1GBASE-SR")

        with check_time():
            response = requests.post(f"{live_server}/resources/assign-interface", json=payload)
        data = response.json()

        assert response.status_code == 200
        assert data["phy_speed"] == "1G"
        assert data["location"] == "London"
        assert data["optics"] == "1GBASE-SR"
        assert data["assigned"] is True


    def test_wrong_query_live(self, live_server, create_payload, check_time):
        payload = create_payload(location="Olesnica", phy_speed="10G", optics="10GBASE-SR")

        with check_time():
            response = requests.post(f"{live_server}/resources/assign-interface", json=payload)
        data = response.json()

        assert response.status_code == 404
        assert data == {"detail": "No resources with specified parameters available"}


    def test_empty_query_live(self, live_server, create_payload, check_time):
        payload = create_payload()

        with check_time():
            response = requests.post(f"{live_server}/resources/assign-interface", json=payload)
        data = response.json()

        assert response.status_code == 400
        assert data == {"detail": "You must provide at least one resource parameter"}


    def test_check_reserved(self, live_server, create_payload, check_time):
        payload = create_payload(optics="10GBASE-LR")

        for _ in range(4):
            with check_time():
                response = requests.post(f"{live_server}/resources/assign-interface", json=payload)
            data = response.json()

            assert response.status_code == 200
            assert data["phy_speed"] == "10G"
            assert data["assigned"] is True

        with check_time():
            response = requests.post(f"{live_server}/resources/assign-interface", json=payload)
        data = response.json()
        assert response.status_code == 404
        assert data == {"detail": "No resources with specified parameters available"}
