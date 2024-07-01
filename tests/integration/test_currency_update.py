import asyncio

import pytest
from fastapi_utils.tasks import repeat_every

from src.repository.currency import currency_repo
from src.repository.rabbitmq import rabbit_mq
from src.service.currency import currency_service


@repeat_every(seconds=2, max_repetitions=1)
async def fake_task():
    await currency_service.get_currency_from_cbr_api()

@pytest.mark.asyncio
@pytest.mark.usefixtures("clear_redis_repository")
@pytest.mark.integration_currency_update
async def test_success_update():
    await rabbit_mq.connect()
    await rabbit_mq.consume_messages('currency_queue', currency_service.update)
    await fake_task()

    first_check = await currency_repo.delete("value")

    assert first_check is None
    await asyncio.sleep(3)

    check = await currency_repo.get("value")
    assert check
