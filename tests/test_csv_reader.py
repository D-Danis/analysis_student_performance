# Тесты для app.reader.CSVReader
# Проверяем:
# - корректное чтение валидного CSV с одной и несколькими строками
# - пропуск строк без имени студента
# - обработка нечисловой оценки -> RecordParseError
# - отсутствие обязательных заголовков -> CSVFormatError
# - отсутствие файла -> FileReadError
#
# Запуск
# pytest -q tests/test_csv_reader.py
import pytest

from app.reader import CSVReader, Record
from app.errors import CSVFormatError, RecordParseError, FileReadError


def test_read_single_file_success(write_csv_fn):
    header = ["student_name", "subject", "teacher_name", "date", "grade"]
    p = write_csv_fn("one.csv", header, [["Ivan", "Math", "Petrov", "2021-09-01", "4.5"]])
    reader = CSVReader([p])
    records = list(reader)
    assert len(records) == 1
    r = records[0]
    assert isinstance(r, Record)
    assert r.student_name == "Ivan"
    assert r.subject == "Math"
    assert r.teacher_name == "Petrov"
    assert r.date == "2021-09-01"
    assert r.grade == 4.5


def test_skip_empty_student_name(write_csv_fn):
    header = "student_name", "subject", "teacher_name", "date", "grade"
    rows = [["", "Math", "Petrov", "2021-09-01", "5"],\
            ["  ", "Bio", "Sidorov", "2021-09-02", "4"],\
            ["Olga", "Chem", "Ivanov", "2021-09-03", "3"]]
    p = write_csv_fn("skip.csv", header, rows)
    reader = CSVReader([str(p)])
    records = list(reader)
    assert len(records) == 1
    assert records[0].student_name == "Olga"


def test_read_multiple_files_and_rows(write_csv_fn):
    header = "student_name", "subject", "teacher_name", "date", "grade"
    p1 = write_csv_fn("a.csv", header, [["A", "S1", "T1", "2021-01-01", "5.0"]])
    p2 = write_csv_fn("b.csv", header, [["B", "S2", "T2", "2021-02-02", "3.2"],\
                                        ["C", "S3", "T3", "2021-03-03", "4.0"]])
    reader = CSVReader([str(p1), str(p2)])
    records = list(reader)
    assert [r.student_name for r in records] == ["A", "B", "C"]


@pytest.mark.parametrize("badrow, errmsgsubstr", 
    [(["Igor", "Math", "Petrov", "2021-09-01", "not-a-number"], "Invalid grade"),
    ('', "Required columns missing"),  # пустой файл/некорректный header проверяется отдельным кейсом ниже
])
def test_invalid_grade_and_missing_columns(write_csv_fn, badrow, errmsgsubstr):
    header = "student_name", "subject", "teacher_name", "date", "grade"
    p = write_csv_fn("bad.csv", header, badrow) if badrow else write_csv_fn("badheader.csv",\
        ["studentname", "subject", "date"], ["Anna", "Math", "2021-09-01"])
    # reader = CSVReader(p)
    reader = CSVReader([str(p)])
    if errmsgsubstr == "Invalid grade":
        with pytest.raises(RecordParseError) as ei:
            list(reader)
        assert errmsgsubstr in str(ei.value)
    else:
        with pytest.raises(CSVFormatError) as ei:
            list(reader)
        assert errmsgsubstr in str(ei.value)


def test_missing_header_raises_CSVFormatError(tmp_path):
    p = tmp_path / "noheader.csv"
    p.write_text("", encoding="utf-8")
    reader = CSVReader([str(p)])
    with pytest.raises(CSVFormatError):
        list(reader)


def test_file_notfound_raises_FileReadError():
    reader = CSVReader(["nonexistentfile12345.csv"])
    with pytest.raises(FileReadError):
        list(reader)