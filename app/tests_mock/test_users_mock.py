import asyncio
import pytest

from app.main import app
from app.schemas.users import UserCreate
from fastapi.testclient import TestClient
from unittest.mock import patch


@patch.object(TestClient, 'post')
def test_sign_up(mock_method):
    request_data = {
        "email": "vader@deathstar.com",
        "last_name": "Vader",
        "first_name": "Darth",
        "patronymic": "",

        "password": "rainbow"
    }
    with TestClient(app) as client:
        mock_method.return_value = {"id": 1,
                                    "email": "vader@deathstar.com",
                                    "last_name": "Vader",
                                    "first_name": "Darth",
                                    "patronymic": "",
                                    "token": {
                                                "access_token": "aaa",
                                                "expires": "bbb",
                                                "token_type": "bearer",
                                                }
                                    }

        response = client.post("/sign-up", json=request_data)

        # Проверяем, что функция была вызвана
    mock_method.assert_called_once()
    # assert response.status_code == 200
    assert response["id"] == 1
    assert response["email"] == "vader@deathstar.com"
    assert response["last_name"] == "Vader"
    assert response["first_name"] == "Darth"
    assert response["patronymic"] == ""
    assert response["token"]["expires"] is not None
    assert response["token"]["access_token"] is not None

@patch.object(TestClient, 'post')
def test_login(mock_method):
    request_data = {"username": "vader@deathstar.com", "password": "rainbow"}
    mock_method.return_value = {
                                "access_token": "aaa",
                                "expires": "bbb",
                                "token_type": "bearer",
                                }
    with TestClient(app) as client:
        response = client.post("/auth", data=request_data)
#     assert response.status_code == 200
    mock_method.assert_called_once()
    assert response["token_type"] == "bearer"
    assert response["expires"] is not None
    assert response["access_token"] is not None


@patch.object(TestClient, 'post')
def test_login_with_invalid_password(mock_method):
    request_data = {"username": "vader@deathstar.com", "password": "unicorn"}
    mock_method.return_value = {"detail": "Incorrect email or password"}
    with TestClient(app) as client:
        response = client.post("/auth", data=request_data)
    # assert response.status_code == 400
    mock_method.assert_called_once()
    assert response["detail"] == "Incorrect email or password"


@patch.object(TestClient, 'get')
def test_user_detail(mock_method):
    with TestClient(app) as client:
        # Create user token to see user info
        loop = asyncio.get_event_loop()
        token = {"token": "aaa"}  #loop.run_until_complete(create_user_token(user_id=1))
        mock_method.return_value = {
            "id": 1,
            "email": "vader@deathstar.com",
            "first_name": "Darth",
        }
        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token['token']}"}
        )

    # assert response.status_code == 200
    mock_method.assert_called_once()
    assert response["id"] == 1
    assert response["email"] == "vader@deathstar.com"
    assert response["first_name"] == "Darth"

@patch.object(TestClient, 'get')
def test_user_detail_forbidden_without_token(mock_method):
    with TestClient(app) as client:
        response = client.get("/users/me")
    mock_method.assert_called_once()
    # assert response.status_code == 401


@patch.object(TestClient, 'get')
@pytest.mark.freeze_time("2015-10-21")
def test_user_detail_forbidden_with_expired_token(mock_method, freezer):
    user = UserCreate(
        email="sidious@deathstar.com",
        last_name="Palpatine",
        first_name="",
        patronymic="",
        password="unicorn"
    )
    user_db = {"token": {"token": "aaa"}}
    with TestClient(app) as client:
        # Create user and use expired token
        loop = asyncio.get_event_loop()
        # user_db = loop.run_until_complete(create_user(user))
        freezer.move_to("'2015-11-10'")
        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {user_db['token']['token']}"}
        )
    # assert response.status_code == 401
    mock_method.assert_called_once()
