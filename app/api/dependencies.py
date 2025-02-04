from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

from app.api.schemes.user import User
from app.utils.unitofwork import IUnitOfWork, UnitOfWork
from app.services.crud_services import UserCRUDService, TaskCRUDService
from app.core.security import authentication

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]


async def get_user_crud_service(uow: UOWDep) -> UserCRUDService:
    return UserCRUDService(uow)


async def get_task_crud_service(uow: UOWDep) -> TaskCRUDService:
    return TaskCRUDService(uow)


user_crud_dep = Annotated[UserCRUDService, Depends(get_user_crud_service)]
task_crud_dep = Annotated[TaskCRUDService, Depends(get_task_crud_service)]
user_oauth2 = Annotated[OAuth2PasswordRequestForm, Depends()]


async def check_user(userdata: user_oauth2, user_crud: user_crud_dep) -> User:
    user = await user_crud.get_user(username=userdata.username)
    return authentication(userdata, user)
