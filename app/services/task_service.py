from app.api.schemes.task import Task, TaskFromDB, TaskUpdate
from app.api.schemes.user import UserFromDB
from app.exc.exception import TaskNotFoundError
from app.utils.unitofwork import IUnitOfWork


class TaskCRUDService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_task(self, creator_id: int, task: Task) -> TaskFromDB:
        data = task.model_dump()
        data.update(creator_id=creator_id)
        async with self.uow:
            task = await self.uow.task_crud.add_task(data=data)
            await self.uow.commit()
            return TaskFromDB.model_validate(task)

    async def get_task(self, creator_id: int, task_id: int) -> TaskFromDB:
        async with self.uow:
            task = await self.uow.task_crud.get_task(creator_id, task_id)
            await self.uow.commit()
            if not task:
                raise TaskNotFoundError
            return TaskFromDB.model_validate(task)

    async def get_task_by_name(self, creator_id: int, task_name: str) -> TaskFromDB:
        async with self.uow:
            task = await self.uow.task_crud.get_task_by_name(creator_id, task_name)
            await self.uow.commit()
            if not task:
                raise TaskNotFoundError
            return TaskFromDB.model_validate(task)

    async def get_tasks(self, creator_id: int) -> list[TaskFromDB]:
        async with self.uow:
            tasks = await self.uow.task_crud.get_tasks(creator_id)
            await self.uow.commit()
            return [TaskFromDB.model_validate(task) for task in tasks]

    async def get_users(self, task_id: int) -> list[UserFromDB]:
        async with self.uow:
            users = await self.uow.task_crud.get_users(task_id)
            await self.uow.commit()
            return [UserFromDB.model_validate(user) for user in users]

    async def update_task(
        self, creator_id: int, task_id: int, task: TaskUpdate
    ) -> TaskFromDB:
        data = task.model_dump()
        async with self.uow:
            task = await self.uow.task_crud.update_task(creator_id, task_id, data)
            await self.uow.commit()
            if not task:
                raise TaskNotFoundError
            return TaskFromDB.model_validate(task)

    async def clear_task(self, creator_id: int, task_id: int):
        async with self.uow:
            result = await self.uow.task_crud.clear_task(creator_id, task_id)
            await self.uow.commit()
            if not result:
                raise TaskNotFoundError
            return result

    async def clear_all_tasks(self, creator_id: int):
        async with self.uow:
            result = await self.uow.task_crud.clear_all_tasks(creator_id)
            await self.uow.commit()
            if not result:
                raise TaskNotFoundError
            return result
