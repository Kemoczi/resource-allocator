

def test_root(test_client, check_time):
    with check_time():
        response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, this is resource allocator! ;)"}


def test_resources(test_client, check_time):
    with check_time():
        response = test_client.get("/resources/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 10


def test_assign_if_by_speed(test_client, create_payload, check_time):
    payload = create_payload(phy_speed="100G")

    with check_time():
        response = test_client.post("/resources/assign-interface", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["phy_speed"] == "100G"
    assert data["assigned"] is True


def test_assign_if_by_speed_location(test_client, create_payload, check_time):
    payload = create_payload(location="London", phy_speed="100G")

    with check_time():
        response = test_client.post("/resources/assign-interface", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["phy_speed"] == "100G"
    assert data["location"] == "London"
    assert data["optics"] == "100GBASE-LR"
    assert data["assigned"] is True


def test_assign_if_by_speed_location_optics(test_client, create_payload, check_time):
    payload = create_payload(location="London", phy_speed="1G", optics="1GBASE-SR")

    with check_time():
        response = test_client.post("/resources/assign-interface", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["phy_speed"] == "1G"
    assert data["location"] == "London"
    assert data["optics"] == "1GBASE-SR"
    assert data["assigned"] is True


def test_wrong_query(test_client, create_payload, check_time):
    payload = create_payload(location="Olesnica", phy_speed="10G", optics="10GBASE-SR")

    with check_time():
        response = test_client.post("/resources/assign-interface", json=payload)
    data = response.json()

    assert response.status_code == 404
    assert data == {"detail": "No resources with specified parameters available"}


def test_empty_query(test_client, create_payload, check_time):
    payload = create_payload()

    with check_time():
        response = test_client.post("/resources/assign-interface", json=payload)
    data = response.json()

    assert response.status_code == 400
    assert data == {"detail": "You must provide at least one resource parameter"}


def test_check_reserved(test_client, create_payload, check_time):
    payload = create_payload(optics="10GBASE-LR")

    for _ in range(4):
        with check_time():
            response = test_client.post("/resources/assign-interface", json=payload)
        data = response.json()

        assert response.status_code == 200
        assert data["phy_speed"] == "10G"
        assert data["assigned"] is True

    with check_time():
        response = test_client.post("/resources/assign-interface", json=payload)
    data = response.json()
    assert response.status_code == 404
    assert data == {"detail": "No resources with specified parameters available"}
