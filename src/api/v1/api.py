from fastapi import APIRouter

from src.api.v1.endpoints import currency

api_router = APIRouter()


api_router.include_router(currency.router, prefix="/currency", tags=["currency"])

