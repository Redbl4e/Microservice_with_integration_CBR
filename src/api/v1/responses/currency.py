from fastapi import status

from src.api.v1.responses.base import ErrorSchema

CURRENCY_GET_RESPONSES = {
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorSchema,
        "content": {
            "application/json": {
                "examples": {
                    404: {
                        "summary": "Валюта не найдена",
                        "value": {
                            "detail": {
                                "code": 404,
                                "reason": "Валюта не найдена"
                            }
                        },
                    }
                }
            }
        },
    },
}