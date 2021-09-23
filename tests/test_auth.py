import pytest
import asyncio
from typing import Generator
from fastapi.testclient import TestClient
from tests.utils.user import create_test_user


def test_user_auth(client: TestClient, event_loop: asyncio.AbstractEventLoop):
    """Test registration of user"""
    test_auth = client.post(
        "/auth/register",
        json={
            "username": "test1",
            "email": "test@gmail.com",
            "full_name": "Test User",
            "role": "Barber",
            "password": "password",
        },
    )
    assert test_auth
    assert test_auth.status_code == 200, test_auth
    data = test_auth.json()
    assert data["status"] == "OK"
    assert data["detail"] == "User has been created successfully"
    test_user_id = data["id"]

    """Test registration of user with incorect type of credatnials"""
    test_auth_incorrect_type = client.post(
        "/auth/register",
        json={
            "username": "test2",
            "email": "1",
            "full_name": "Test User",
            "role": "Barber",
            "password": "password",
        },
    )
    assert not test_auth_incorrect_type
    assert test_auth_incorrect_type.status_code == 422, test_auth_incorrect_type
    data = test_auth_incorrect_type.json()
    assert data["detail"][0]["msg"] == "value is not a valid email address"

    response = client.post(
        "/auth/login",
        data={
            "grant_type": "",
            "username": "test1",
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

    # """Test get one user"""
    # test_get_user = client.get(
    #     f"/auth/user?pk={test_user_id}", headers={"Authorization": f"Bearer {token}"}
    # )
    # assert test_get_user
    # assert test_get_user.status_code == 200, test_get_user
    # data = test_get_user.json()
    # assert data["username"] == "Ernest"

    # """Test logout endpoint"""
    # logout = client.post(
    #     "/auth/logout",
    #     headers={"Authorization": f"Bearer {token}"},
    # )
    # assert logout
    # assert logout.status_code == 200, logout
    # data = logout.json()
    # assert data["is_active"] == False
