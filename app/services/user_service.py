from sqlalchemy.exc import IntegrityError

from app.db.models import Users
from app.utils.unitofwork import IUnitOfWork
from app.api.schemes.user import UserFromDB, UserReg, User
from app.exc.exception import (
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.core.security import create_hash


class UserCRUDService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_user(self, user: UserReg) -> UserFromDB:
        data = user.model_dump()
        data.update(password=create_hash(data["password"]))
        async with self.uow:
            try:
                user: Users = await self.uow.user_crud.add_user(data)
                await self.uow.commit()
                return UserFromDB.model_validate(user)
            except IntegrityError:
                raise UserAlreadyExistsError

    async def get_user(
        self, user_id: int | None = None, username: str | None = None
    ) -> UserFromDB:
        async with self.uow:
            if user_id:
                user: Users = await self.uow.user_crud.get_by_id(user_id)
            elif username:
                user: Users = await self.uow.user_crud.get_user_by_username(username)
            await self.uow.commit()
            if not user:
                raise UserNotFoundError
            return UserFromDB.model_validate(user)

    async def update_user(self, user_id: int, user: User):
        async with self.uow:
            await self.uow.user_crud.update_by_username(user_id, user.model_dump())
            await self.uow.commit()
