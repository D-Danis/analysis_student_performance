import csv
import pytest
from typing import List
from pathlib import Path

from app.datastore import DataStore
from app.reader import Record


def write_csv(path: Path, header: List[str], rows: List[List|str]):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


@pytest.fixture
def write_csv_fn(tmp_path):
    def _write(name: str, header: list[str], rows: list[list]):
        p = tmp_path / name
        write_csv(p, header, rows)
        return str(p)
    return _write


@pytest.fixture
def sample_records():
    def makerecord(name: str, subject: str, teacher: str, date: str, grade: float):
        return Record(student_name=name, subject=subject, teacher_name=teacher, date=date, grade=grade)
    return makerecord


@pytest.fixture
def datastore():
    return DataStore()


@pytest.fixture
def populated_datastore(sample_records, datastore):
    records = (
        sample_records("Ivan", "Math", "Petrov", "2021-09-01", 5.0),
        sample_records("Ivan", "Math", "Petrov", "2021-09-02", 4.0),
        sample_records("Olga", "Chem", "Ivanov", "2021-09-01", 3.5),
        sample_records("Olga", "Chem", "Ivanov", "2021-09-02", 4.5),
    )
    datastore.add_records(records)
    return datastore