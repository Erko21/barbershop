import json
import pytest
import asyncio

from fastapi.testclient import TestClient
import requests
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

    """Test creation of proposition"""
    proposition_created_response = client.post(
        "/proposition/create",
        json={"name": "Hair cut", "price": 300.00, "job_time": 1.5},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert proposition_created_response
    assert proposition_created_response.status_code == 200, proposition_created_response
    data = proposition_created_response.json()
    assert data["id"] == 1
    first_proposition_id = data["id"]
    first_proposition_price = data["price"]
    first_proposition_job_time = data["job_time"]

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
        f"/proposition/{first_proposition_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert get_one_proposition
    assert get_one_proposition.status_code == 200, get_one_proposition
    data = get_one_proposition.json()
    assert data["id"] == 1
    assert data["name"] == "Hair cut"

    """Test proposition filtered by price"""
    proposition_by_price = client.get(
        f"/proposition/by_price?price={first_proposition_price}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert proposition_by_price
    assert proposition_by_price.status_code == 200, proposition_by_price
    data = proposition_by_price.json()
    assert len(data) == 1
    assert data[0]["price"] == 300.00

    """Test proposition filtered by time"""
    proposition__by_time = client.get(
        f"/proposition/by_time?time={first_proposition_job_time}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert proposition__by_time
    assert proposition__by_time.status_code == 200, proposition__by_time
    data = proposition__by_time.json()
    assert len(data) == 1
    assert data[0]["job_time"] == 1.5

    """Test propositiom update"""
    proposition_update = client.post(
        f"/proposition/update?pk={first_proposition_id}",
        json={"price": 400.00},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert proposition_update
    assert proposition_update.status_code == 200, proposition_update
    data = proposition_update.json()
    assert data["status"] == "OK"
    assert data["detail"] == "Proposition has been updated successfully"
    assert data["price"] == 400

    """Test proposition delete"""
    proposition_delete = client.post(
        f"/proposition/delete?pk={first_proposition_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert proposition_delete
    assert proposition_delete.status_code == 204, proposition_delete
