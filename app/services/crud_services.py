from app.utils.unitofwork import IUnitOfWork
from sqlalchemy.exc import IntegrityError

from app.api.schemes.user import UserRegistration, UserFromDB
from app.exc.exception import UserAlreadyExistsError, UserNotFoundError
from app.core.security import create_hash


class UserCRUDService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_user(self, user: UserRegistration):
        user.password = create_hash(user.password)
        async with self.uow:
            try:
                res = await self.uow.user_crud.add_one(user.model_dump())
                await self.uow.commit()
                return res
            except IntegrityError:
                raise UserAlreadyExistsError

    async def get_user(
        self, user_id: int | None = None, username: str | None = None
    ) -> UserFromDB:
        async with self.uow:
            if user_id:
                user = await self.uow.user_crud.get_by_id(user_id)
            elif username:
                user = await self.uow.user_crud.find_by_username(username)
            await self.uow.commit()
            if not user:
                raise UserNotFoundError
            return UserFromDB(
                user_id=user.id,
                username=user.username,
                password=user.password,
                role=user.role,
            )


class TaskCRUDService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow
