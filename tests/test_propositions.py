import pytest
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
            is_superuser=True,
            password="password",
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

    """Test creation of proposition"""
    proposition_created_response = client.post(
        "/proposition/create",
        data={"proposition_name": "Hair cut", "price": 300, "job_time": 1.5},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert proposition_created_response
    assert proposition_created_response.status_code == 200, proposition_created_response
    data = proposition_created_response.json()
    assert data["status"] == "OK"
    assert data["detail"] == "Proposition has been successfully created"
    first_proposition_id = data["id"]

    """Test proposition delete"""
    proposition_delete = client.post(
        f"/proposition/delete_{first_proposition_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert proposition_delete
    assert proposition_delete.status_code == 200, proposition_delete
    data = proposition_delete.json()
    assert data["status"] == "OK"
    assert data["detail"] == "Proposition has been successfully deleted"

    """Test propositiom update"""
    proposition_update = client.post(
        f"/proposition/update_{first_proposition_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert proposition_update
    assert proposition_update.status_code == 200, proposition_update
    data = proposition_update.json()
    assert data["status"] == "OK"
    assert data["detail"] == "Proposition has been successfully updated"

    """Test get all propositions"""
    get_all_propositions = client.get(
        "/proposition/get_all",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert get_all_propositions
    assert get_all_propositions.status_code == 200, get_all_propositions
    data = get_all_propositions.json()
    assert len(data) > 0

    """Test get one proposition"""
    get_one_proposition = client.get(
        f"/proposition/get_one_{first_proposition_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert get_one_proposition
    assert get_one_proposition.status_code == 200, get_one_proposition
    data = get_one_proposition.json()
    assert data["id"] == 1
    assert data["proposition_name"] == "Hair cut"

    """Test proposition filtered by price"""
    proposition_by_price = client.get(
        "/proposition/by_pryce",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert proposition_by_price
    assert proposition_by_price.status_code == 200, proposition_by_price
    data = proposition_by_price.json()
    assert data["price"] == 300

    """Test proposition filtered by time"""
    proposition__by_time = client.get(
        "/proposition/by_time",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert proposition__by_time
    assert proposition__by_time.status_code == 200, proposition__by_time
    data = proposition__by_time.json()
    assert data["job_time"] == 1.5
