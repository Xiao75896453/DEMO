import pytest
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from src.api.account.query import get_account
from src.main import ACCOUNT_API_ROUTE

from lib.custom_response import failed_response
from lib.unit_test import everything_equals


class TestCreateAccount:
    CREATE_ACCOUNT_API_ROUTE = ACCOUNT_API_ROUTE

    @pytest.mark.asyncio
    async def test_create_account(self, test_client: TestClient):
        test_data = {
            "username": "123",
            "password": "Test1234",
        }
        test_client.post(self.CREATE_ACCOUNT_API_ROUTE, json=test_data)

        expected_result = {
            "id": 1,
            "username": test_data["username"],
            "password": everything_equals,
            "failed_attempts": 0,
            "failed_login_time": None,
        }

        account = await get_account(username=test_data["username"])

        assert jsonable_encoder(account) == expected_result

    @pytest.mark.asyncio
    async def test_create_account_failed_because_username_too_short(
        self, test_client: TestClient
    ):
        test_data = {
            "username": "12",
            "password": "Test1234",
        }

        response = test_client.post(self.CREATE_ACCOUNT_API_ROUTE, json=test_data)

        expected_response = failed_response(reason="Username is too short")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json() == expected_response

    @pytest.mark.asyncio
    async def test_create_account_failed_because_username_too_long(
        self, test_client: TestClient
    ):
        test_data = {
            "username": "123456789012345678901234567890123",
            "password": "Test1234",
        }

        response = test_client.post(self.CREATE_ACCOUNT_API_ROUTE, json=test_data)

        expected_response = failed_response(reason="Username is too long")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json() == expected_response

    @pytest.mark.asyncio
    async def test_create_account_failed_because_username_exist(
        self, test_client: TestClient
    ):
        test_data = {
            "username": "123",
            "password": "Test1234",
        }

        test_client.post(self.CREATE_ACCOUNT_API_ROUTE, json=test_data)

        response = test_client.post(self.CREATE_ACCOUNT_API_ROUTE, json=test_data)

        expected_response = failed_response(reason="Username already exists")

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json() == expected_response

    @pytest.mark.asyncio
    async def test_create_account_failed_because_password_too_short(
        self, test_client: TestClient
    ):
        test_data = {
            "username": "123",
            "password": "1234567",
        }

        response = test_client.post(self.CREATE_ACCOUNT_API_ROUTE, json=test_data)

        expected_response = failed_response(reason="Password is too short")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json() == expected_response

    @pytest.mark.asyncio
    async def test_create_account_failed_because_password_too_long(
        self, test_client: TestClient
    ):
        test_data = {
            "username": "123",
            "password": "123456789012345678901234567890123",
        }

        response = test_client.post(self.CREATE_ACCOUNT_API_ROUTE, json=test_data)

        expected_response = failed_response(reason="Password is too long")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json() == expected_response

    @pytest.mark.asyncio
    async def test_create_account_failed_because_password_not_contain_uppercase_letter(
        self, test_client: TestClient
    ):
        test_data = {
            "username": "123",
            "password": "test1234",
        }

        response = test_client.post(self.CREATE_ACCOUNT_API_ROUTE, json=test_data)

        expected_response = failed_response(
            reason="Password not contain at least 1 uppercase letter, 1 lowercase letter, and 1 number"
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json() == expected_response

    @pytest.mark.asyncio
    async def test_create_account_failed_because_password_not_contain_lowercase_letter(
        self, test_client: TestClient
    ):
        test_data = {
            "username": "123",
            "password": "TEST1234",
        }

        response = test_client.post(self.CREATE_ACCOUNT_API_ROUTE, json=test_data)

        expected_response = failed_response(
            reason="Password not contain at least 1 uppercase letter, 1 lowercase letter, and 1 number"
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json() == expected_response

    @pytest.mark.asyncio
    async def test_create_account_failed_because_password_not_contain_number(
        self, test_client: TestClient
    ):
        test_data = {
            "username": "123",
            "password": "TestTest",
        }

        response = test_client.post(self.CREATE_ACCOUNT_API_ROUTE, json=test_data)

        expected_response = failed_response(
            reason="Password not contain at least 1 uppercase letter, 1 lowercase letter, and 1 number"
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json() == expected_response
