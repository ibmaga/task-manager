from typing import Annotated
from fastapi import APIRouter, status, WebSocket, Query, WebSocketDisconnect

from app.api.schemes.task import Task, TaskFromDB, TaskUpdate
from app.api.dependencies import task_crud_dep, check_access_dep
from app.exc.models import ErrorResponseModel
from app.utils.websockets import websockets_manager

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponseModel}},
)
async def write_task(
    task: Annotated[Task, Query()],
    task_crud: task_crud_dep,
    jwt_payload: check_access_dep,
) -> TaskFromDB:
    result = await task_crud.add_task(jwt_payload.id, task)
    await websockets_manager.broadcast(f"New task: {result}")
    return result


@router.get("/{task_id}")
async def get_task(
    task_id: int, task_crud: task_crud_dep, jwt_payload: check_access_dep
) -> TaskFromDB:
    return await task_crud.get_task(jwt_payload.id, task_id)


@router.get("/get_all/")
async def get_all_tasks(
    task_crud: task_crud_dep, jwt_payload: check_access_dep
) -> list[TaskFromDB]:
    return await task_crud.get_tasks(jwt_payload.id)


@router.patch("/{task_id}")
async def update_task(
    task_id: int,
    task: Annotated[TaskUpdate, Query()],
    task_crud: task_crud_dep,
    jwt_payload: check_access_dep,
) -> TaskFromDB:
    return await task_crud.update_task(jwt_payload.id, task_id, task)


@router.delete("/{task_id}")
async def delete_task(
    task_id: int, task_crud: task_crud_dep, jwt_payload: check_access_dep
):
    return await task_crud.clear_task(jwt_payload.id, task_id)


@router.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websockets_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await websockets_manager.disconnect(websocket)
