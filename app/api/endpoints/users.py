from fastapi import APIRouter, Depends

from app.api.dependencies import user_crud_dep, CheckPermission
from app.api.schemes.user import UserOut

router = APIRouter(prefix="/users", tags=["users"])


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    user_crud: user_crud_dep,
    permissions=Depends(CheckPermission()),
) -> UserOut:
    """Удаление пользователя"""
    return await user_crud.delete_user(user_id)
