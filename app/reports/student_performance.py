from typing import List, Tuple
from tabulate import tabulate

from app.reports.base import ReportBase
from app.datastore import DataStore


class StudentPerformanceReport(ReportBase):
    name = "student-performance"

    def __init__(self, datastore: DataStore, precision: int = 2, top: int | None = None) -> None:
        super().__init__(datastore)
        self.precision = precision
        self.top = top
        self._rows: List[Tuple[str, float]] = []
        

    def build(self) -> None:
        averages = self.datastore.get_student_averages()
        rows = list(averages.items())
        rows.sort(key=lambda x: (-x[1], x[0]))
        if self.top is not None:
            rows = rows[: self.top]
        self._rows = rows

    def render(self) -> str:
        headers = ["Student", "Average"]
        table = [(name, f"{avg:.{self.precision}f}") for name, avg in self._rows]
        return tabulate(table, headers=headers, tablefmt="github", stralign="left", numalign="right")
    
    
    
import logging
logging.basicConfig(level=logging.INFO)

logging.info("start student")

# class StudentPerformanceReport(ReportBase):
#     name = 'student-performance'

#     def __init__(self, datastore: DataStore, precision: int = 2) -> None:
#         super().__init__(datastore)
#         self.precision = precision
#         self._rows: List[Tuple[str, float]] = []
#         logging.info("init finish")

#     def build(self) -> None:
#         averages = self.datastore.get_student_averages()
#         rows = list(averages.items())
#         # sort by average desc, then name asc
#         rows.sort(key=lambda x: (-x[1], x[0]))
#         self._rows = rows
#         logging.info("build finish")

#     def render(self) -> str:
        
#         headers = ['student_name', 'Average']
#         table = [(name, f'{avg:.{self.precision}f}') for name, avg in self._rows]
#         logging.info("render finish")
#         return tabulate(table, headers=headers, tablefmt='github', stralign='left', numalign='right')
