from src.exceptions import ProjectException


class RepositoryException(ProjectException):
    reason = "Ошибка репозитория"


class NoResultFound(RepositoryException):
    reason = "Объект не найден, когда требовался один"
