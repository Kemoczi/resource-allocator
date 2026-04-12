import pytest
import requests


FIELD_VALUE = [
        ("location", "London"),
        ("phy_speed", "100G"),
        ("optics", "10GBASE-SR")
    ]


@pytest.mark.testclient
class TestWithClient:

    @pytest.mark.parametrize("field, value", FIELD_VALUE)
    def test_assign_by_single_param(self, test_client, create_payload, field, value):
        payload = create_payload(**{field: value})

        response = test_client.post("/resources/assign-interface", json=payload)
        data = response.json()

        assert response.status_code == 200
        assert data[field] == value
        assert data["assigned"] is True

    @pytest.mark.parametrize("location, phy_speed", [("London", "100G"), ("London", "10G")])
    def test_assign_by_location_speed(self, test_client, create_payload, location, phy_speed):
        payload = create_payload(location=location, phy_speed=phy_speed)

        response = test_client.post("/resources/assign-interface", json=payload)
        data = response.json()

        assert response.status_code == 200
        assert data["location"] == location
        assert data["phy_speed"] == phy_speed
        assert data["assigned"] is True

    @pytest.mark.parametrize(
        "location, phy_speed, optics",
        [("London", "1G", "1GBASE-SR"), ("London", "10G", "10GBASE-SR")]
    )
    def test_assign_by_location_speed_optics(
            self, test_client, create_payload, location, phy_speed, optics
    ):
        payload = create_payload(location=location, phy_speed=phy_speed, optics=optics)

        response = test_client.post("/resources/assign-interface", json=payload)
        data = response.json()

        assert response.status_code == 200
        assert data["location"] == location
        assert data["phy_speed"] == phy_speed
        assert data["optics"] == optics
        assert data["assigned"] is True

    @pytest.mark.parametrize("field, value", FIELD_VALUE)
    def test_check_reserved(self, test_client, create_payload, field, value):
        payload = create_payload(**{field: value})

        response = test_client.get("/resources/")
        data = response.json()
        num_of_resources = 0
        for item in data:
            if item[field] == value and item["assigned"] == False:
                num_of_resources += 1

        for _ in range(num_of_resources):
            response = test_client.post("/resources/assign-interface", json=payload)
            data = response.json()

            assert response.status_code == 200
            assert data[field] == value
            assert data["assigned"] is True

        response = test_client.post("/resources/assign-interface", json=payload)
        data = response.json()
        assert response.status_code == 404
        assert data == {"detail": "No resources with specified parameters available"}

    @pytest.mark.parametrize("field, value", [("location", "London")])
    def test_resource_exhaustion(self, test_client, create_payload, field, value):
        payload = create_payload(**{field: value})

        while True:
            response = test_client.post("/resources/assign-interface", json=payload)
            if response.status_code == 404:
                break
            assert response.status_code == 200

        response = test_client.get("/resources/free")
        assert response.status_code == 404
        data = response.json()
        assert data == {"detail": "No free resources available"}


@pytest.mark.live
class TestLiveServer:

    @pytest.mark.parametrize("field, value", [("phy_speed", "100G")])
    def test_assign_by_single_param_live(
            self, live_server, create_payload, field, value, check_time
    ):
        payload = create_payload(**{field: value})

        with check_time():
            response = requests.post(
                f"{live_server}/resources/assign-interface", json=payload, timeout=3
            )
        data = response.json()

        assert response.status_code == 200
        assert data[field] == value
        assert data["assigned"] is True

    @pytest.mark.parametrize("location, phy_speed", [("London", "100G")])
    def test_assign_by_speed_location_live(
            self, live_server, create_payload, location, phy_speed, check_time
    ):
        payload = create_payload(location=location, phy_speed=phy_speed)

        with check_time():
            response = requests.post(
                f"{live_server}/resources/assign-interface", json=payload, timeout=3
            )
        data = response.json()

        assert response.status_code == 200
        assert data["location"] == location
        assert data["phy_speed"] == phy_speed
        assert data["assigned"] is True

    @pytest.mark.parametrize("location, phy_speed, optics", [("London", "1G", "1GBASE-SR")])
    def test_assign_by_speed_location_optics_live(
            self, live_server, create_payload, location, phy_speed, optics, check_time
    ):
        payload = create_payload(location=location, phy_speed=phy_speed, optics=optics)

        with check_time():
            response = requests.post(
                f"{live_server}/resources/assign-interface", json=payload, timeout=3
            )
        data = response.json()

        assert response.status_code == 200
        assert data["location"] == location
        assert data["phy_speed"] == phy_speed
        assert data["optics"] == optics
        assert data["assigned"] is True

    @pytest.mark.parametrize("field, value", [("optics", "10GBASE-LR")])
    def test_check_reserved_live(self, live_server, create_payload, field, value, check_time):
        payload = create_payload(**{field: value})

        with check_time():
            response = requests.get(f"{live_server}/resources/", timeout=3)
        data = response.json()
        num_of_resources = 0
        for item in data:
            if item[field] == value and item["assigned"] == False:
                num_of_resources += 1

        for _ in range(num_of_resources):
            with check_time():
                response = requests.post(
                    f"{live_server}/resources/assign-interface", json=payload, timeout=3
                )
            data = response.json()

            assert response.status_code == 200
            assert data[field] == value
            assert data["assigned"] is True

        with check_time():
            response = requests.post(
                f"{live_server}/resources/assign-interface", json=payload, timeout=3
            )
        data = response.json()
        assert response.status_code == 404
        assert data == {"detail": "No resources with specified parameters available"}
