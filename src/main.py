import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.v1.api import api_router
from src.repository.rabbitmq import rabbit_mq
from src.service.currency import currency_service
from src.tasks.update_currency import update_currencies_every_24_hours


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbit_mq.connect()
    await rabbit_mq.declare_queue(queue_name="currency_queue")
    await rabbit_mq.consume_messages('currency_queue', currency_service.update)
    await currency_service.get_currency_from_cbr_api()
    await update_currencies_every_24_hours()
    yield


app = FastAPI(
    root_path="/api/v1",
    lifespan=lifespan
)

app.include_router(api_router)
