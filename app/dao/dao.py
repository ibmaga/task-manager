from typing import Sequence
from sqlalchemy import select, delete, insert, update, and_

from app.dao.base_dao import CRUD
from app.db.models import Users, Tasks


class UserCrud(CRUD):
    model = Users

    async def add_user(self, data: dict) -> model:
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get_user_by_username(self, username: str) -> model:
        stmt = select(self.model).where(self.model.username == username)
        result = await self.session.execute(stmt)
        user = result.scalar_one()
        return user

    async def update_by_username(self, user_id: int, data: dict) -> model:
        stmt = (
            update(self.model)
            .where(self.model.id == user_id)
            .values(**data)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()


class TaskCrud(CRUD):
    model = Tasks

    async def add_task(self, data: dict) -> model:
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get_task(self, creator_id: int, task_id: int) -> model | None:
        stmt = select(self.model).where(
            and_(self.model.id == task_id, self.model.creator_id == creator_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_task_by_name(self, creator_id: int, task_name: str) -> model:
        stmt = select(self.model).where(
            and_(self.model.name == task_name, self.model.creator_id == creator_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_tasks(self, creator_id: int) -> Sequence[model]:
        stmt = select(self.model).where(self.model.creator_id == creator_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_task(
        self, creator_id: int, task_id: int, data: dict
    ) -> model | None:
        stmt = (
            update(self.model)
            .where(and_(self.model.id == task_id, self.model.creator_id == creator_id))
            .values(**data)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def clear_task(self, creator_id: int, task_id: int):
        stmt = (
            delete(self.model)
            .where(and_(self.model.id == task_id, self.model.creator_id == creator_id))
            .returning(self.model.id)
        )
        result = await self.session.execute(stmt)
        return result
