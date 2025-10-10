import csv
from dataclasses import dataclass
from typing import (
                    Iterable,
                    Iterator,
                    List
                    )

from app.errors import (
                        FileReadError,
                        CSVFormatError,
                        RecordParseError
                        )


@dataclass
class Record:
    student_name: str
    subject: str
    teacher_name: str
    date: str
    grade: float


class CSVReader:
    REQUIRED_FIELDS = {
        "student_name",
        "subject",
        "teacher_name",
        "date",
        "grade"
        }

    def __init__(self, 
                 paths: Iterable[str], 
                 encoding: str = "utf-8") -> None:
        self.paths: List[str] = list(paths)
        self.encoding = encoding

    def __iter__(self) -> Iterator[Record]:
        for path in self.paths:
            try:
                with open(path,
                          newline="",
                          encoding=self.encoding) as fh:
                    reader = csv.DictReader(fh)
                    if not reader.fieldnames:
                        raise CSVFormatError(
                            f"Empty or missing header in {path}",
                            code="csv.header.missing")
                    fields = {fn.strip() for fn in reader.fieldnames if fn}
                    if not self.REQUIRED_FIELDS.issubset(fields):
                        raise CSVFormatError(
                            f"Required columns missing in {path}",
                            code="csv.columns.missing")
                    for line_no, row in enumerate(reader, start=2):
                        try:
                            name = (row.get("student_name") or "").strip()
                            if not name:
                                # пропускаем записи без имени
                                continue
                            grade_raw = (row.get("grade") or "").strip()
                            grade = float(grade_raw)
                            yield Record(
                                student_name=name,
                                subject=(row.get("subject") or "").strip(),
                                teacher_name=(row.get("teacher_name") or "").strip(),
                                date=(row.get("date") or "").strip(),
                                grade=grade,
                            )
                        except ValueError:
                            raise RecordParseError(
                                f"Invalid grade at {path}:{line_no}",
                                code="record.grade.invalid")
            except FileNotFoundError as exc:
                raise FileReadError(f"File not found: {path}") from exc
            except OSError as exc:
                raise FileReadError(f"Error reading file: {path}") from exc
            