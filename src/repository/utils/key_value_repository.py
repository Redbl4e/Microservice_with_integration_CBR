from abc import abstractmethod, ABC
from typing import Generic, TypeVar, Any, Iterable

MODEL = TypeVar("MODEL")


class KeyValueRepositoryABC(Generic[MODEL], ABC):
    base_key: str

    @abstractmethod
    async def get(self, key: str) -> dict:
        """
        Получить запись по ключу

        :param key: Ключ записи
        :raises NoResultFound: Не найдено ни одной записи
        :return: Найденная запись
        """
        raise NotImplementedError

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """
        Проверяет есть ли такая запись

        :param key: Ключ записи
        :returns: True, если запись есть
        """
        raise NotImplementedError

    @abstractmethod
    async def filter(self, key_pattern: str) -> list[dict[str, Any]]:
        """
        Отфильтровать записи

        :param key_pattern: Паттерн, которому должны удовлетворять ключи
        :return: Список найденных записей
        """
        raise NotImplementedError

    @abstractmethod
    async def create(self, key: str, data: MODEL, **kwargs) -> dict:
        """
        Создать новую запись

        :param key: Ключ записи
        :param data: Данные для создания записи
        :raises RepositoryException: Ошибка при добавлении
        :return: Созданная запись
        """
        raise NotImplementedError

    @abstractmethod
    async def update(
        self, key: str, data: dict[str, Any], fields: Iterable[str], **kwargs
    ) -> dict:
        """
        Обновить запись

        :param key: Ключ записи
        :param data: Данные для обновления записи
        :param fields: Итерируемый объект, с названиями полей для обновления
        :raises IntegrityError: Ошибка уникальности полей
        :raises NoResultFound: Не найдено ни одной записи
        :raises RepositoryException: Ошибка при обновлении
        :return: Обновлённая запись
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str, **kwargs) -> None:
        """
        Удалить запись

        :param key: Ключ записи
        :return: None
        """
        raise NotImplementedError

