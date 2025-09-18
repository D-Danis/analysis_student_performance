from typing import Dict, Type

from app.errors import ReportError
from app.datastore import DataStore
from app.reports.base import ReportBase
from app.reports.student_performance import StudentPerformanceReport
from app.reports.teacher_performance import TeacherPerformanceReport
from app.reports.subject_performance import SubjectPerformanceReport


class ReportFactory:
    """
    Фабрика отчётов. Легко добавить новый отчёт — зарегистрировать его здесь.
    """
    _registry: Dict[str, Type[ReportBase]] = {
        StudentPerformanceReport.name: StudentPerformanceReport,
        TeacherPerformanceReport.name: TeacherPerformanceReport,
        SubjectPerformanceReport.name: SubjectPerformanceReport,
    }

    @classmethod
    def create(cls, name: str, datastore: DataStore, **kwargs: object) -> ReportBase:
        ctor = cls._registry.get(name)
        if not ctor:
            raise ReportError(f"Unknown report: {name}", code="report.unknown")
        return ctor(datastore, **kwargs)