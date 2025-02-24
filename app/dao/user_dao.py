from sqlalchemy import select, delete, insert, update

from app.dao.base_dao import CRUD
from app.db.models import User


class UserCrud(CRUD):
    model = User

    async def add_user(self, data: dict) -> model:
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_user_by_username(self, username: str) -> model:
        stmt = select(self.model).where(self.model.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_user_by_id(self, user_id: int, data: dict) -> model:
        stmt = (
            update(self.model)
            .where(self.model.id == user_id)
            .values(**data)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_user_by_id(self, user_id: int) -> model:
        stmt = delete(self.model).where(self.model.id == user_id).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
