from app.db.models import User
from app.utils.unitofwork import IUnitOfWork
from app.api.schemes.user import UserFromDB, UserReg, User
from app.utils.hasher import hasher
from app.log.log import logger
from app.exc.exception import (
    UserAlreadyExistsError,
    UserNotFoundError,
    AuthenticationError,
)


class UserCRUDService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_user(self, user: UserReg) -> UserFromDB:
        data = user.model_dump()
        data.update(password=hasher.hash(data["password"]))
        async with self.uow:
            user_db = await self.uow.user_crud.get_user_by_username(data["username"])
            if not user_db:
                user: User = await self.uow.user_crud.add_user(data)
                await self.uow.commit()
                return UserFromDB.model_validate(user)

            raise UserAlreadyExistsError

    async def get_user(
        self,
        user_id: int | None = None,
        username: str | None = None,
    ) -> UserFromDB:
        async with self.uow:
            if user_id:
                user = await self.uow.user_crud.get_by_id(user_id)
            elif username:
                user = await self.uow.user_crud.get_user_by_username(username)
            else:
                logger.error("No user_id or username provided")
                raise ValueError("No user_id or username provided")
            await self.uow.commit()

            if not user:
                raise AuthenticationError
            return UserFromDB.model_validate(user)

    async def update_user(self, user_id: int, user: User) -> UserFromDB:
        async with self.uow:
            result = await self.uow.user_crud.update_user_by_id(
                user_id, user.model_dump()
            )
            await self.uow.commit()

            if not result:
                raise UserNotFoundError
            return UserFromDB.model_validate(result)

    async def delete_user(self, user_id: int) -> UserFromDB:
        async with self.uow:
            result = await self.uow.user_crud.delete_user_by_id(user_id)
            await self.uow.commit()

            if not result:
                raise UserNotFoundError
            return UserFromDB.model_validate(result)
