import pytest

from tests.integration.test_redis import test_redis_repo


@pytest.fixture
async def clear_redis_repository():
    yield

    await test_redis_repo.redis.flushdb()
    await test_redis_repo.redis.connection_pool.disconnect()
