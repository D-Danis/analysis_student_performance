# Analysis of student performance

Простой скрипт для обработки csv-файла

---

## Описание

Проект реализует чтение файлы с данными  об успеваемости студентов и формирование отчетов,
возможность получение топа и точности отчета

---

## Стек технологий

- Python 3.12
- Pytest
- pytest-cov
- tabulate
- argparse

---

## Структура проекта

```
analysis_student_performance/
├─ app/                             # Каталог приложение
│  ├─ __init__.py
│  ├─ reports/                      # Каталог для генерации отчетов
│  │  ├─ __init__.py
│  │  ├─ base.py                    # Базовый класс для генерации отчетов
│  │  ├─ registry.py                # Класс для регистрации отчетов
│  │  ├─ student_performance.py     # Класс для генерации отчетов 
│  │  ├─ subject_performance.py     # Класс для генерации отчетов
│  │  └─ teacher_performance.py     # Класс для генерации отчетов
│  ├─ cli.py                        # Основной код обработки
│  ├─ datastore.py                  # Классы для хранение данных
│  ├─ errors.py                     # Классы для ошибок
│  └─ reader.py                     # Классы для чтение файлов
├─ tests/                           # Каталог с тестами
│  ├─ conftest.py                   # Каталог с тестами
│  ├─ test_cli.py                   # Тест код обработки
│  ├─ test_csv_reader.py            # Тест чтение файлов
│  ├─ test_datastore.py             # Тест хранение данных
│  └─ test_reports.py               # Тест генерации отчетов
├── .gitignore                      # gitignore 
├── requirements.txt                # Зависимости проекта
├── students1.csv                   # файл для проверки 1
├── students2.csv                   # файл для проверки 2
├── README.md                       # Этот файл
└─ main.py                          # Точка входа
```

---

## Быстрый старт

### 1. Клонировать репозиторий

```bash
git clone https://github.com/D-Danis/analysis_student_performance.git
cd app
```

### 2. Создайте виртуальное окружение (рекомендуется)

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

---

## Пример работы операции

- вывода среднего успеваемости студентов

```sh
python3 main.py --file students1.csv students2.csv --report student-performance 
```

- вывода среднего по учителям топ 5

```sh
python3 main.py --file students1.csv students2.csv --report teacher-performance --top 5
```

- вывода среднего по придметам с точностью 3

```sh
python3 main.py --file students1.csv students2.csv --report subject-performance --precision 3 
```

---

## Запуск тестов

Для запуска всех тестов используйте команду:

```bash
pytest --maxfail=1 --disable-warnings -v
```

```sh
pytest --maxfail=1 --disable-warnings -v                 
============================= test session starts ==============================
platform linux -- Python 3.12.7, pytest-8.4.1, pluggy-1.6.0 -- */.venv/bin/python3
cachedir: .pytest_cache
rootdir: */analysis_student_performance
plugins: cov-6.2.1
collected 36 items                                                             

tests/test_cli.py::test_parse_args_basic PASSED                          [  2%]
tests/test_cli.py::test_run_success PASSED                               [  5%]
tests/test_cli.py::test_run_app_error PASSED                             [  8%]
tests/test_cli.py::test_run_unexpected_exception PASSED                  [ 11%]
tests/test_csv_reader.py::test_read_single_file_success PASSED           [ 13%]
tests/test_csv_reader.py::test_skip_empty_student_name PASSED            [ 16%]
tests/test_csv_reader.py::test_read_multiple_files_and_rows PASSED       [ 19%]
tests/test_csv_reader.py::test_invalid_grade_and_missing_columns[badrow0-Invalid grade] PASSED [ 22%]
tests/test_csv_reader.py::test_invalid_grade_and_missing_columns[-Required columns missing] PASSED [ 25%]
tests/test_csv_reader.py::test_missing_header_raises_CSVFormatError PASSED [ 27%]
tests/test_csv_reader.py::test_file_notfound_raises_FileReadError PASSED [ 30%]
tests/test_datastore.py::test_empty_datastore_behaviour PASSED           [ 33%]
tests/test_datastore.py::test_get_student_averages PASSED                [ 36%]
tests/test_datastore.py::test_get_teacher_averages PASSED                [ 38%]
tests/test_datastore.py::test_get_subject_averages PASSED                [ 41%]
tests/test_datastore.py::test_top_n_ordering_and_limit PASSED            [ 44%]
tests/test_reports.py::test_student_build[ds0-expected0-extra0-expectation0] PASSED [ 47%]
tests/test_reports.py::test_student_build[ds1-expected1-extra1-expectation1] PASSED [ 50%]
tests/test_reports.py::test_student_render_precision PASSED              [ 52%]
tests/test_reports.py::test_student_render_empty PASSED                  [ 55%]
tests/test_reports.py::test_report_factory_kwargs_passed[extra0] PASSED  [ 58%]
tests/test_reports.py::test_report_factory_kwargs_passed[extra1] PASSED  [ 61%]
tests/test_reports.py::test_report_factory_kwargs_passed[extra2] PASSED  [ 63%]
tests/test_reports.py::test_report_factory_kwargs_passed[extra3] PASSED  [ 66%]
tests/test_reports.py::test_report_factory_kwargs_passed[extra4] PASSED  [ 69%]
tests/test_reports.py::test_report_factory_kwargs_passed[extra5] PASSED  [ 72%]
tests/test_reports.py::test_report_factory_positive_negative[non-existent-report-expectation0] PASSED [ 75%]
tests/test_reports.py::test_report_factory_positive_negative[student-performance-expectation1] PASSED [ 77%]
tests/test_reports.py::test_report_factory_positive_negative[teacher-performance-expectation2] PASSED [ 80%]
tests/test_reports.py::test_report_factory_positive_negative[subject-performance-expectation3] PASSED [ 83%]
tests/test_reports.py::test_report_factory_registered_reports[StudentPerformanceReport-expectation0] PASSED [ 86%]
tests/test_reports.py::test_report_factory_registered_reports[TeacherPerformanceReport-expectation1] PASSED [ 88%]
tests/test_reports.py::test_report_factory_registered_reports[SubjectPerformanceReport-expectation2] PASSED [ 91%]
tests/test_reports.py::test_report_factory_registered_reports[non-existent-report-expectation3] PASSED [ 94%]
tests/test_reports.py::test_create_and_isinstance[<lambda>-True-True] PASSED [ 97%]
tests/test_reports.py::test_create_and_isinstance[<lambda>-True-False] PASSED [100%]

============================== 36 passed in 0.09s ============================
```

---

## Проверка покрытия тестами

Для измерения покрытия кода используйте плагин `pytest-cov`. 

Запустите тесты с покрытием:

```bash
pytest --cov=tests --cov-report=term-missing:skip-covered
```

Результат
```sh
pytest --cov=tests --cov-report=term-missing:skip-covered
============================= test session starts ==============================
platform linux -- Python 3.12.7, pytest-8.4.1, pluggy-1.6.0
rootdir: */analysis_student_performance
plugins: cov-6.2.1
collected 36 items                                                             

tests/test_cli.py ....                                                   [ 11%]
tests/test_csv_reader.py .......                                         [ 30%]
tests/test_datastore.py .....                                            [ 44%]
tests/test_reports.py ....................                               [100%]

================================ tests coverage ================================
_______________ coverage: platform linux, python 3.12.7-final-0 ________________

Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
tests/test_cli.py          68      1    99%   42
tests/test_reports.py      90      5    94%   28, 170-172, 174, 176
-----------------------------------------------------
TOTAL                     275      6    98%

4 files skipped due to complete coverage.
============================== 36 passed in 0.48s ==============================

```