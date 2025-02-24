from fastapi import APIRouter, Depends

from app.api.dependencies import user_crud_dep
from app.api.middlewares.middlewares import CheckPermission

router = APIRouter(prefix="/users", tags=["users"])


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    user_crud: user_crud_dep,
    permissions=Depends(CheckPermission()),
):
    return await user_crud.delete_user(user_id)
