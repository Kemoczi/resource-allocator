import pytest

from app.models import Resource


@pytest.mark.testclient
def test_check_cleanup(test_client, testing_db_session, create_payload, check_time):
    param = "London"
    payload = create_payload(location=param)

    assign_counter = 0
    while True:
        with check_time():
            response = test_client.post("/resources/assign-interface", json=payload)
        if response.status_code == 404:
            break
        assert response.status_code == 200
        assign_counter += 1
    assert assign_counter > 0

    with check_time():
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

    with check_time():
        response = test_client.get("/resources/")
    assert response.status_code == 200
    data = response.json()
    for item in data:
        assert item["assigned"] == False
