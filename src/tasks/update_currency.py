from fastapi_utils.tasks import repeat_every

from src.service.currency import currency_service


@repeat_every(seconds=60*60*24)
async def update_currencies_every_24_hours():
    await currency_service.get_currency_from_cbr_api()
