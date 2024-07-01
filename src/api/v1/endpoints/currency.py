from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from src.api.v1.dependencies import CurrencyServiceDependency
from src.api.v1.responses.currency import CURRENCY_GET_RESPONSES
from src.schemas.schemas import Rate, CurrencyResult
from src.service.exceptions import CurrencyNotExist

router = APIRouter()


@router.get(
    "",
    summary="Значение Валюты",
    operation_id="currency:get_value",
    response_model=CurrencyResult,
    responses=CURRENCY_GET_RESPONSES
)
async def get_currency(
        params: Annotated[Rate, Depends(Rate)],
        service: CurrencyServiceDependency
):
    try:
        result = await service.get_currency(params)
        return result
    except CurrencyNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": 400,
                "reason": e.reason
            }
        )
