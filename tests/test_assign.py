import pytest
import requests


@pytest.mark.testclient
class TestWithClient:

    def test_assign_if_by_speed(self, test_client, create_payload):
        payload = create_payload(phy_speed="100G")

        response = test_client.post("/resources/assign-interface", json=payload)
        data = response.json()

        assert response.status_code == 200
        assert data["phy_speed"] == "100G"
        assert data["assigned"] is True


    def test_assign_if_by_speed_location(self, test_client, create_payload):
        payload = create_payload(location="London", phy_speed="100G")

        response = test_client.post("/resources/assign-interface", json=payload)
        data = response.json()

        assert response.status_code == 200
        assert data["phy_speed"] == "100G"
        assert data["location"] == "London"
        assert data["optics"] == "100GBASE-LR"
        assert data["assigned"] is True


    def test_assign_if_by_speed_location_optics(self, test_client, create_payload):
        payload = create_payload(location="London", phy_speed="1G", optics="1GBASE-SR")

        response = test_client.post("/resources/assign-interface", json=payload)
        data = response.json()

        assert response.status_code == 200
        assert data["phy_speed"] == "1G"
        assert data["location"] == "London"
        assert data["optics"] == "1GBASE-SR"
        assert data["assigned"] is True


    def test_check_reserved(self, test_client, create_payload):
        param = "10GBASE-LR"
        payload = create_payload(optics=param)

        response = test_client.get("/resources/")
        data = response.json()
        num_of_resources = 0
        for item in data:
            if item["optics"] == param and item["assigned"] == False:
                num_of_resources += 1

        for _ in range(num_of_resources):
            response = test_client.post("/resources/assign-interface", json=payload)
            data = response.json()

            assert response.status_code == 200
            assert data["phy_speed"] == "10G"
            assert data["assigned"] is True

        response = test_client.post("/resources/assign-interface", json=payload)
        data = response.json()
        assert response.status_code == 404
        assert data == {"detail": "No resources with specified parameters available"}


@pytest.mark.live
class TestLiveServer:

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


    def test_check_reserved_live(self, live_server, create_payload, check_time):
        param = "10GBASE-LR"
        payload = create_payload(optics=param)

        with check_time():
            response = requests.get(f"{live_server}/resources/")
        data = response.json()
        num_of_resources = 0
        for item in data:
            if item["optics"] == param and item["assigned"] == False:
                num_of_resources += 1

        for _ in range(num_of_resources):
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
