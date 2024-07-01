import xml.etree.ElementTree as ET
from typing import AsyncGenerator

import aiohttp
import sys

from src.core.config.settings import settings
from src.repository.currency import currency_repo
from src.repository.exceptions import NoResultFound, RepositoryException
from src.repository.rabbitmq import rabbit_mq
from src.schemas.schemas import Rate, CurrencyResult
from src.service.exceptions import CurrencyServiceError, CurrencyNotExist


class CurrencyService:
    """Сервис по работе с валютами"""

    def __init__(self):
        self.rabbitmq = rabbit_mq
        self.currency_redis = currency_repo

    async def get_currency(self, currency: Rate) -> CurrencyResult:
        """ Получить валюту
        :param currency: RateEnum c валютой
        :raises CurrencyNotExist: Валюта не найдена
        """
        try:
            data = await self.currency_redis.get(key="value")
            value = data.get(currency.name)

            if value is None:
                raise CurrencyNotExist

            result = CurrencyResult(name=currency.name, value=value)

            return result
        except NoResultFound:
            raise CurrencyNotExist

    async def update(self, message: dict):
        """ Обновить данные, полученные при подписке на событие.
         Эта функция вызывается при добавлении данных в очередь RabbitMQ.
         """
        try:
            await self.currency_redis.create(key="value", data=message)
        except RepositoryException:
            raise CurrencyServiceError("Ошибка пр обновлении")

    async def get_currency_from_cbr_api(self):
        """Получить данные из API и отправить их в очередь"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(settings.API.CURRENCY_API_URL) as response:
                    data = await response.text()

            currencies = dict()
            root = ET.fromstring(data)

            for item in root.findall('Valute'):
                name = item.find('Name').text
                value = item.find('Value').text
                currencies[name] = value
            await self.rabbitmq.send_message(
                'currency_queue', currencies
            )
        except aiohttp.ClientError:
            raise CurrencyServiceError("Ошибка интеграции с API")
        except ET.ParseError:
            raise CurrencyServiceError("Ошибка парсинга XML")
        except RepositoryException:
            raise CurrencyServiceError("Ошибка добавления в очередь")


currency_service = CurrencyService()


async def get_currency_service() -> AsyncGenerator[CurrencyService, None]:
    yield CurrencyService()
