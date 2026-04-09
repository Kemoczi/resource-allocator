
def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, this is resource allocator! ;)"}


def test_resources(test_client):
    response = test_client.get("/resources/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 10


def test_assign_interface_by_speed(test_client, create_payload):
    payload = create_payload(phy_speed="10G")

    response = test_client.post("/resources/assign-interface", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["phy_speed"] == "10G"
    assert data["assigned"] is True


def test_check_reserved(test_client, create_payload):
    payload = create_payload(optics="100GBASE-ER")

    response = test_client.post("/resources/assign-interface", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["phy_speed"] == "100G"
    assert data["assigned"] is True

    response = test_client.post("/resources/assign-interface", json=payload)
    data = response.json()
    assert response.status_code == 404
    assert data == {"detail": "No resources with specified parameters available"}
