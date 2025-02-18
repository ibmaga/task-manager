import pytest
import pytest_asyncio
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


global task_id


@pytest.mark.asyncio(loop_scope="session")
class TestTasks:

    @staticmethod
    async def test_create_task(ac: AsyncClient):
        global task_id
        data = {"name": "test", "description": "testtest"}
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await ac.post("/tasks/", params=data, headers=headers)

        assert response.status_code == 201
        assert response.json()

        task_id = response.json().get("id")
        print(task_id)

    @staticmethod
    async def test_get_task(ac: AsyncClient):
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await ac.get(f"/tasks/{task_id}", headers=headers)

        assert response.status_code == 200
        assert response.json()

    @staticmethod
    async def test_update_task(ac: AsyncClient):
        data = {"status": "at work"}
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await ac.patch(f"/tasks/{task_id}", params=data, headers=headers)

        assert response.status_code == 200
        assert response.json()

    @staticmethod
    async def test_get_tasks(ac: AsyncClient):
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await ac.get("/tasks/get_all/", headers=headers)

        assert response.status_code == 200
        assert response.json()

    @staticmethod
    async def test_delete_task(ac: AsyncClient):
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await ac.delete(f"/tasks/{task_id}", headers=headers)

        assert response.status_code == 200
