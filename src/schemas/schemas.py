from pydantic import BaseModel, ConfigDict
from fastapi import Query
from pydantic import Field
from decimal import Decimal

from src.core.types.currency import Currency


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )


class Rate(BaseSchema):
    name: Currency = Field(Query(default_factory=None))


class CurrencyResult(BaseSchema):
    name: str
    value: str
