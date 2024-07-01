from src.repository.exceptions import NoResultFound
from src.repository.redis import RedisRepository
import pytest


class RedisTestRepo(RedisRepository):
    base_key = "test"


test_redis_repo = RedisTestRepo()


@pytest.fixture(scope="function")
async def populate_redis_repository():
    await test_redis_repo.create(
        "test",
        {"test": "test"},
    )
    yield




@pytest.mark.integration_redis
class TestRedisRepository:
    @pytest.mark.usefixtures("populate_redis_repository", "clear_redis_repository")
    async def test_success_get(self):
        result = await test_redis_repo.get("test")

        assert result == {"test": "test"}

    @pytest.mark.usefixtures("clear_redis_repository")
    async def test_error_no_result_found_get(self):
        with pytest.raises(NoResultFound):
            await test_redis_repo.get("test")

    @pytest.mark.usefixtures("clear_redis_repository")
    async def test_success_create(self):
        await test_redis_repo.create("test", {"test": "test"})
        result = await test_redis_repo.get("test")

        assert result == {'test': 'test'}
