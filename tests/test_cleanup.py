import pytest

from app.models import Resource


@pytest.mark.testclient
def test_check_cleanup(test_client, testing_db_session, create_payload):
    # This test assumes the current seeded inventory consists entirely of London resources.
    param = "London"
    payload = create_payload(location=param)

    assign_counter = 0
    while True:
        response = test_client.post("/resources/assign-interface", json=payload)
        if response.status_code == 404:
            break
        assert response.status_code == 200
        assign_counter += 1
    assert assign_counter > 0

    response = test_client.get("/resources/")
    assert response.status_code == 200
    data = response.json()
    for item in data:
        assert item["assigned"] == True

    # Cleanup as in app.free_resources.py
    testing_db_session.query(Resource).filter(Resource.assigned == True).update(
        {Resource.assigned: False}
    )
    testing_db_session.commit()

    response = test_client.get("/resources/")
    assert response.status_code == 200
    data = response.json()
    for item in data:
        assert item["assigned"] == False
