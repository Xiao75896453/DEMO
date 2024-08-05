from datetime import datetime, timedelta

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from freezegun import freeze_time
from src.api.authentication.controller import (
    BLOCK_VERIFICATION_TIME, MAX_FAILED_VERIFICATION_ATTEMPTS)
from src.main import ACCOUNT_API_ROUTE, AUTHENTICATION_API_ROUTE

from lib.custom_response import failed_response, success_response


class TestVerification:
    CREATE_ACCOUNT_API_ROUTE = ACCOUNT_API_ROUTE
    VERIFICATION_API_ROUTE = f"{AUTHENTICATION_API_ROUTE}/verification"

    @pytest.mark.asyncio
    async def test_verification(self, test_client: TestClient):
        test_data = {
            "username": "123",
            "password": "Test1234",
        }
        test_client.post(self.CREATE_ACCOUNT_API_ROUTE, json=test_data)

        response = test_client.post(self.VERIFICATION_API_ROUTE, json=test_data)

        expected_response = success_response()

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response

    @pytest.mark.asyncio
    async def test_verification_failed_because_username_not_exists(
        self, test_client: TestClient
    ):
        test_data = {
            "username": "123",
            "password": "Test1234",
        }
        test_client.post(self.CREATE_ACCOUNT_API_ROUTE, json=test_data)

        failed_data = {
            "username": "1234",
            "password": "Test1234",
        }
        response = test_client.post(self.VERIFICATION_API_ROUTE, json=failed_data)

        expected_response = failed_response(reason="Username not exists")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == expected_response

    @pytest.mark.asyncio
    async def test_verification_failed_because_password_not_correct(
        self, test_client: TestClient
    ):
        test_data = {
            "username": "123",
            "password": "Test1234",
        }
        test_client.post(self.CREATE_ACCOUNT_API_ROUTE, json=test_data)

        failed_data = {
            "username": "123",
            "password": "not_correct",
        }
        response = test_client.post(self.VERIFICATION_API_ROUTE, json=failed_data)

        expected_response = failed_response(reason="Password is not correct")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == expected_response

    @pytest.mark.asyncio
    async def test_verification_failed_because_too_many_attempts(
        self, test_client: TestClient
    ):
        test_data = {
            "username": "123",
            "password": "Test1234",
        }
        test_client.post(self.CREATE_ACCOUNT_API_ROUTE, json=test_data)

        failed_data = {
            "username": "123",
            "password": "not_correct",
        }
        for _ in range(MAX_FAILED_VERIFICATION_ATTEMPTS + 1):
            response = test_client.post(self.VERIFICATION_API_ROUTE, json=failed_data)

        expected_response = failed_response(
            reason="Too many failed verification attempts, blocking one minutes"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == expected_response

    @pytest.mark.asyncio
    async def test_verification_failed_because_password_not_correct_after_block_time(
        self, test_client: TestClient
    ):
        test_data = {
            "username": "123",
            "password": "Test1234",
        }
        test_client.post(self.CREATE_ACCOUNT_API_ROUTE, json=test_data)

        failed_data = {
            "username": "123",
            "password": "not_correct",
        }
        initial_datetime = datetime(
            year=2024, month=1, day=1, hour=0, minute=0, second=0
        )
        with freeze_time(initial_datetime) as frozen_datetime:
            for _ in range(MAX_FAILED_VERIFICATION_ATTEMPTS + 1):
                test_client.post(self.VERIFICATION_API_ROUTE, json=failed_data)

            frozen_datetime.move_to(
                initial_datetime + BLOCK_VERIFICATION_TIME + timedelta(seconds=1)
            )
            response = test_client.post(self.VERIFICATION_API_ROUTE, json=failed_data)

        expected_response = failed_response(reason="Password is not correct")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == expected_response

    @pytest.mark.asyncio
    async def test_verification_after_block_time(self, test_client: TestClient):
        test_data = {
            "username": "123",
            "password": "Test1234",
        }
        test_client.post(self.CREATE_ACCOUNT_API_ROUTE, json=test_data)

        failed_data = {
            "username": "123",
            "password": "not_correct",
        }
        initial_datetime = datetime(
            year=2024, month=1, day=1, hour=0, minute=0, second=0
        )
        with freeze_time(initial_datetime) as frozen_datetime:
            for _ in range(MAX_FAILED_VERIFICATION_ATTEMPTS + 1):
                test_client.post(self.VERIFICATION_API_ROUTE, json=failed_data)

            frozen_datetime.move_to(
                initial_datetime + BLOCK_VERIFICATION_TIME + timedelta(seconds=1)
            )
            response = test_client.post(self.VERIFICATION_API_ROUTE, json=test_data)

        expected_response = success_response()

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response
