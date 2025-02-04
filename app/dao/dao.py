from sqlalchemy import select, delete
from app.dao.base_crud import CRUD
from app.db.models import Users, Tasks


class UserCrud(CRUD):
    model = Users

    async def find_by_username(self, username: str) -> model:
        stmt = select(self.model).where(self.model.username == username)
        result = await self.session.execute(stmt)
        user = result.scalar_one()
        return user


class TaskCrud(CRUD):
    model = Tasks

    async def get_tasks_by_name(self, task_name: str):
        stmt = select(self.model).where(self.model.name == task_name)
        result = await self.session.execute(stmt)
        return result.scalars()

    async def clear_task(self, task_id: int):
        stmt = (
            delete(self.model).where(self.model.id == task_id).returning(self.model.id)
        )
        result = await self.session.execute(stmt)
        return result
