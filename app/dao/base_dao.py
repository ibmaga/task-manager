from abc import ABC, abstractmethod
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession


class ICRUD(ABC):

    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, ident: int):
        raise NotImplementedError


class CRUD(ICRUD):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> model:
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get_by_id(self, ident: int) -> model:
        result = await self.session.get(self.model, ident)
        return result
