from redis.asyncio import Redis

from app.core.configs import settings


class RedisDB:
    def __init__(self):
        self.redis = Redis.from_url(
            url=settings.redis_url,
            decode_responses=True,
            auto_close_connection_pool=True,
        )

    async def set(self, name: str, value: str):
        await self.redis.setnx(name, value)

    async def get(self, name: str) -> str:
        return await self.redis.get(name)

    async def delete(self, name: str):
        await self.redis.delete(name)

    async def keys(self):
        return self.redis.keys()
