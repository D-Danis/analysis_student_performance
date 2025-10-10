from typing import List, Tuple
from tabulate import tabulate

from app.reports.base import ReportBase
from app.datastore import DataStore


class TeacherPerformanceReport(ReportBase):
    name = "teacher-performance"

    def __init__(self,
                 datastore: DataStore,
                 precision: int = 2,
                 top: int | None = None) -> None:
        super().__init__(datastore)
        self.precision = precision
        self.top = top
        self._rows: List[Tuple[str, float]] = []

    def build(self) -> None:
        averages = self.datastore.get_teacher_averages()
        rows = list(averages.items())
        rows.sort(key=lambda x: (-x[1], x[0]))
        if self.top is not None:
            rows = rows[: self.top]
        self._rows = rows

    def render(self) -> str:
        headers = ["Teacher", "Average"]
        table = [(name,
                  f"{avg:.{self.precision}f}")
                 for name, avg in self._rows]
        return tabulate(table, 
                        headers=headers, 
                        tablefmt="github", 
                        stralign="left", 
                        numalign="right")