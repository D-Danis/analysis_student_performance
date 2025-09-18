from collections import defaultdict
from typing import Dict, Iterable, List

from app.reader import Record


class DataStore:
    """Хранилище агрегированных данных."""
    def __init__(self) -> None:
        self._student_grades: Dict[str, List[float]] = defaultdict(list)
        self._teacher_grades: Dict[str, List[float]] = defaultdict(list)
        self._subject_grades: Dict[str, List[float]] = defaultdict(list)
    
    def add_record(self, record: Record) -> None:
        self._student_grades[record.student_name].append(record.grade)
        if record.teacher_name:
            self._teacher_grades[record.teacher_name].append(record.grade)
        if record.subject:
            self._subject_grades[record.subject].append(record.grade)

    def add_records(self, records: Iterable[Record]) -> None:
        for r in records:
            self.add_record(r)

    def get_student_averages(self) -> Dict[str, float]:
        return {n: sum(g)/len(g) for n, g in self._student_grades.items() if g}

    def get_teacher_averages(self) -> Dict[str, float]:
        return {n: sum(g)/len(g) for n, g in self._teacher_grades.items() if g}

    def get_subject_averages(self) -> Dict[str, float]:
        return {n: sum(g)/len(g) for n, g in self._subject_grades.items() if g}

    def top_n(self, items: Dict[str, float], n: int = 10):
        return sorted(items.items(), key=lambda x: (-x[1], x[0]))[:n]
 