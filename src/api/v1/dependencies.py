from typing import Annotated
from fastapi import Depends
from src.service.currency import get_currency_service, CurrencyService

# Services
CurrencyServiceDependency = Annotated[CurrencyService, Depends(get_currency_service)]