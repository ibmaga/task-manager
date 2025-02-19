import pytest
from httpx import AsyncClient

global access_token, refresh_token


@pytest.mark.asyncio(loop_scope="session")
class TestAuth:
    @staticmethod
    async def test_reg(ac: AsyncClient):
        data = {"username": "test", "password": "testtest"}
        response = await ac.post("/auth/sign-up/", json=data)

        assert response.status_code == 201

    @staticmethod
    async def test_auth(ac: AsyncClient):
        global access_token, refresh_token
        data = {
            "grant_type": "password",
            "username": "test",
            "password": "testtest",
            "scope": "",
            "client_id": "string",
            "client_secret": "string",
        }
        response = await ac.post("/auth/log-in/", data=data)

        access_token = response.json().get("access_token")
        refresh_token = response.json().get("refresh_token")

        assert response.status_code == 200
        assert access_token
        assert refresh_token

    @staticmethod
    async def test_refresh(ac: AsyncClient):
        global access_token
        headers = {"Authorization": f"Bearer {refresh_token}"}
        response = await ac.post("/auth/refresh/", headers=headers)

        access_token = response.json().get("access_token")

        assert response.status_code == 200
        assert access_token
