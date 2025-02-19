import pytest
from httpx import AsyncClient
from httpx_ws import connect_ws

from tests.test_users import access_token

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

    # @staticmethod
    # async def test_websockets(ac: AsyncClient):
    #     async with aconnect_ws(url="ws://127.0.0.1:8000/tasks/ws/", client=ac) as ws:
    #         message =  await ws.receive_text()
    #         assert message
