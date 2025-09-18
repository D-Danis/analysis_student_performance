from typing import Optional


class AppError(Exception):
    """Базовый класс всех ошибок в приложении."""
    code: Optional[str] = None

    def __init__(self, message: str, *, code: Optional[str] = None) -> None:
        super().__init__(message)
        if code is not None:
            self.code = code


class FileReadError(AppError):
    """Ошибка чтения файла."""
    pass


class CSVFormatError(AppError):
    """Ошибка формата CSV (отсутствующие колонки, некорректный заголовок и т.п.)."""
    pass


class RecordParseError(AppError):
    """Ошибка при парсинге строки в запись (например, нечисловая оценка)."""
    pass


class ReportError(AppError):
    """Ошибка, связанная с генерацией отчёта (например, неизвестный отчёт)."""
    pass