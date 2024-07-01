from src.repository.redis import RedisRepository


class CurrencyRepository(RedisRepository):
    base_key = "currency"


currency_repo = CurrencyRepository()
