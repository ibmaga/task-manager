from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.schemes.other import Payload
from app.api.schemes.user import UserFromDB, UserOut
from app.utils.unitofwork import IUnitOfWork, UnitOfWork
from app.services.task_service import TaskCRUDService
from app.services.user_service import UserCRUDService
from app.core.security import (
    authentication,
    CheckToken,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
)

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]


async def get_user_crud_service(uow: UOWDep) -> UserCRUDService:
    return UserCRUDService(uow)


async def get_task_crud_service(uow: UOWDep) -> TaskCRUDService:
    return TaskCRUDService(uow)


user_crud_dep = Annotated[UserCRUDService, Depends(get_user_crud_service)]
task_crud_dep = Annotated[TaskCRUDService, Depends(get_task_crud_service)]
user_oauth2_dep = Annotated[OAuth2PasswordRequestForm, Depends()]

check_access_dep = Annotated[Payload, Depends(CheckToken(ACCESS_TOKEN_TYPE))]
check_refresh_dep = Annotated[Payload, Depends(CheckToken(REFRESH_TOKEN_TYPE))]


async def check_user(user: user_oauth2_dep, user_crud: user_crud_dep) -> UserOut:
    """Проверка пользователя при авторизации"""
    user_from_db = await user_crud.get_user(username=user.username)
    return await authentication(user, user_from_db, user_crud)


async def get_user_by_payload(
    payload: check_refresh_dep, user_crud: user_crud_dep
) -> UserFromDB:
    """Получение пользователя по payload"""
    user_from_db = await user_crud.get_user(user_id=payload.id)
    return user_from_db
