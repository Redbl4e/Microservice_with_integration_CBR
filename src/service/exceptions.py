from src.exceptions import ProjectException


class CurrencyServiceError(ProjectException):
    reason = "Ошибка сервиса работы с валютами"


class CurrencyNotExist(CurrencyServiceError):
    reason = "Валюта не надйена"
