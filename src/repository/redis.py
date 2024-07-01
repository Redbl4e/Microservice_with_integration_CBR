from json import dumps, loads
from typing import Any, Iterable

from redis import RedisError
from redis.asyncio import Redis

from src.core.config.settings import settings
from src.repository.exceptions import NoResultFound, RepositoryException
from src.repository.utils.key_value_repository import KeyValueRepositoryABC


class RedisRepository(KeyValueRepositoryABC):
    base_key: str

    def __init__(self) -> None:
        self.redis = Redis(
            host=settings.REDIS.HOST,
            port=settings.REDIS.PORT,
            db=settings.REDIS.DATA_DB,
        )

    async def get(self, key: str) -> dict:
        result = await self.redis.get(f"{self.base_key}:{key}")
        if result is None:
            raise NoResultFound

        result_dict = loads(result)
        return result_dict

    async def exists(self, key: str) -> bool:
        try:
            await self.get(key)
        except NoResultFound:
            return False

        return True

    async def filter(self, key_pattern: str) -> list[dict[str, Any]]:
        keys = await self.redis.keys(f"{self.base_key}:{key_pattern}")
        if len(keys) == 0:
            raise NoResultFound
        values = await self.redis.mget(*keys)
        result = []
        for key, values in zip(keys, values):
            dict_values = loads(values.decode())
            result.append({key.decode(): dict_values})
        return result

    async def create(self, key: str, data: dict, **kwargs) -> dict:
        ex = kwargs.get("ex")
        value_str = dumps(data)
        try:
            return await self.redis.set(f"{self.base_key}:{key}", value_str, ex=ex)
        except RedisError:
            raise RepositoryException("Ошибка при добавлении")


    async def update(
            self, key: str, data: dict[str, Any], fields: Iterable[str], **kwargs
    ) -> dict:
        ex = kwargs.get("ex")

        value_str = await self.redis.get(f"{self.base_key}:{key}")
        value_dict = loads(value_str)

        for field_name in fields:
            value_dict[field_name] = data.get(field_name)

        updated_data = dumps(value_dict)

        try:
            await self.redis.set(f"{self.base_key}:{key}", updated_data, ex)
        except RedisError:
            raise RepositoryException("Ошибка при обновлении")

        return value_dict

    async def delete(self, key: str, **kwargs) -> None:
        try:
            await self.redis.delete(f"{self.base_key}:{key}")
        except RedisError:
            raise RepositoryException("Ошибка при удалении")
