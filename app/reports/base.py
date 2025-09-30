from abc import ABC, abstractmethod

from app.datastore import DataStore


class ReportBase(ABC):
    """
    Базовый класс для отчётов. Каждый отчёт должен реализовать методы:
    - build: формирует внутренние данные отчёта из DataStore
    - render: возвращает представление (например, строку для печати)
    """
    name: str

    def __init__(self, datastore: DataStore) -> None:
        self.datastore = datastore

    @abstractmethod
    def build(self) -> None:
        """Собрать внутренние данные для отчёта."""
        raise NotImplementedError

    @abstractmethod
    def render(self) -> str:
        """Вернуть строковое представление отчёта
        (для вывода в консоль)."""
        raise NotImplementedError