# Проверяем:
# - parse_args корректно парсит опции
# - run возвращает 0 и печатает отчёт при нормальной работе
# - run возвращает коды ошибок 1/2 при исключениях
#
# Заготовка использует monkeypatch для подмены зависимостей:
# - app.reader.CSVReader — чтобы не читать реальные файлы
# - app.datastore.DataStore — простой заглушечный datastore
# - app.reports.registry.ReportFactory — фабрика, возвращающая объект с build/render
# - app.errors.AppError — для проверки обработки AppError
#
# Запуск
# pytest -v tests/test_cli.py
import app.cli as cli_module  
from app.errors import AppError


class DummyReader:
    def __init__(self, files):
        self.files = files


class DummyDataStore:
    def __init__(self):
        self.added = False

    def add_records(self, reader):
        self.added = True
        self.last_reader = reader


class DummyReport:
    def __init__(self, datastore, precision=2, top=None):
        self.datastore = datastore
        self.precision = precision
        self.top = top
        self.built = False

    def build(self):
        # имитируем построение
        if not getattr(self.datastore, "added", False):
            raise RuntimeError("datastore not populated")
        self.built = True

    def render(self):
        return f"REPORT precision={self.precision} top={self.top}"


class DummyFactory:
    @staticmethod
    def create(name, datastore, **extra):
        return DummyReport(datastore, precision=extra.get("precision", 2), top=extra.get("top", None))


def test_parse_args_basic():
    argv = ["--files", "a.csv", "b.csv", "--report", "student-performance", "--precision", "3", "--top", "5"]
    ns = cli_module.parse_args(argv)
    assert ns.files == ["a.csv", "b.csv"]
    assert ns.report == "student-performance"
    assert ns.precision == 3
    assert ns.top == 5


def test_run_success(monkeypatch, capsys):
    # Подменяем CSVReader, DataStore и ReportFactory
    monkeypatch.setattr("app.cli.CSVReader", DummyReader)
    monkeypatch.setattr("app.cli.DataStore", DummyDataStore)
    monkeypatch.setattr("app.cli.ReportFactory", DummyFactory)
    rc = cli_module.run(["--files", "f1.csv", "--report", "student-performance", "--precision", "4", "--top", "10"])
    captured = capsys.readouterr()
    assert rc == 0
    assert "REPORT precision=4 top=10" in captured.out


def test_run_app_error(monkeypatch, capsys):
    class BadDataStore(DummyDataStore):
        def add_records(self, reader):
            raise AppError("bad data", code=123)

    monkeypatch.setattr("app.cli.CSVReader", DummyReader)
    monkeypatch.setattr("app.cli.DataStore", BadDataStore)
    monkeypatch.setattr("app.cli.ReportFactory", DummyFactory)
    rc = cli_module.run(["--files", "f.csv", "--report", "student-performance"])
    captured = capsys.readouterr()
    assert rc == 2
    assert "Error 123" in captured.err


def test_run_unexpected_exception(monkeypatch, capsys):
    class BadReport(DummyReport):
        def build(self):
            raise RuntimeError("boom")

    class FactoryBad:
        @staticmethod
        def create(name, datastore, **extra):
            return BadReport(datastore, precision=extra.get("precision", 2), top=extra.get("top", None))

    monkeypatch.setattr("app.cli.CSVReader", DummyReader)
    monkeypatch.setattr("app.cli.DataStore", DummyDataStore)
    monkeypatch.setattr("app.cli.ReportFactory", FactoryBad)
    rc = cli_module.run(["--files", "f.csv", "--report", "student-performance"])
    captured = capsys.readouterr()
    assert rc == 1
    assert "Unexpected error" in captured.err