import asyncio

from fastapi.testclient import TestClient

from tests.utils.user import create_test_user


def test_proposition(client: TestClient, event_loop: asyncio.AbstractEventLoop):
    test_user = event_loop.run_until_complete(
        create_test_user(
            username="Ernest",
            email="ekedesh@gmail.com",
            full_name="Ernest Kedesh",
            role="Admin",
            password="password",
            is_active=True,
        )
    )

    response = client.post(
        "/auth/login",
        data={
            "grant_type": "",
            "username": "Ernest",
            "password": "password",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "accept": "application/json",
        },
        verify=False,
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data["access_token"]) > 0
    token = data["access_token"]

    """Test creation of proposition_response"""
    proposition_response = client.post(
        "/propositions/create",
        json={"name": "Hair cut", "price": 300.00, "job_time": 1.5},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert proposition_response
    assert proposition_response.status_code == 200, proposition_response
    data = proposition_response.json()
    assert data["id"] == 1
    proposition_response_id = data["id"]

    """Test creation of record"""
    record_create = client.post(
        "/records/create",
        json={
            "customer_email": "customer@customer.com",
            "customer_full_name": "Test Customer",
            "customer_phone_number": "+380341234575",
            "proposition_id": proposition_response_id,
            "user_id": test_user.id,
            "time": "2019-07-26T00:00:00",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert record_create
    assert record_create.status_code == 200, record_create
    data = record_create.json()
    assert data["customer_full_name"] == "Test Customer"
    record_id = data["id"]
    record_datetime = data["time"]

    """Test get all records"""
    get_all_records = client.get(
        "/records/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert get_all_records
    assert get_all_records.status_code == 200, get_all_records
    data = get_all_records.json()
    assert len(data) > 0

    """Test get one record"""
    get_one_record = client.get(
        f"/records/get_record?pk={record_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert get_one_record
    assert get_one_record.status_code == 200, get_one_record
    data = get_one_record.json()
    assert data["id"] == 1
    assert data["proposition"]["name"] == "Hair cut"
    assert data["user"]["id"] == 1

    """Test record filtered by date"""
    record_filtered_by_date = client.get(
        f"/records/by_date?date={record_datetime}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert record_filtered_by_date
    assert record_filtered_by_date.status_code == 200, record_filtered_by_date
    data = record_filtered_by_date.json()
    assert len(data) != 1

    """Test update record"""
    record_update = client.post(
        f"/records/update?pk={record_id}",
        json={"customer_full_name": "Customer Test"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert record_update
    assert record_update.status_code == 200, record_update
    data = record_update.json()
    assert data["customer_full_name"] == "Customer Test"

    """Test record delete"""
    record_delete = client.post(
        f"/records/delete?pk={record_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert record_delete
    assert record_delete.status_code == 204, record_delete
