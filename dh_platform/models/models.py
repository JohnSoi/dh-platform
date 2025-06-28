"""Модуль для моделей"""

__author__: str = "Старков Е.П."

from sqlalchemy.orm import DeclarativeBase, declared_attr


class BaseModel(DeclarativeBase):
    """
    Абстрактная базовая модель со стандартными полями

    Examples:
        >>> from dh_platform.models import BaseModel, IDMixin
        >>>
        >>> class User(BaseModel, IDMixin):
        ...     ...
    """

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(self) -> str:
        """Конвертирует CamelCase в snake_case"""
        name = self.__name__
        return name[0].lower() + "".join([f"_{c.lower()}" if c.isupper() else c for c in name[1:]])

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
