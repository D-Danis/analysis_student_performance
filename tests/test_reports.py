import pytest
from contextlib import nullcontext as does_not_raise
from tabulate import tabulate

from app.errors import ReportError
from app.reports.registry import ReportFactory
from app.reports.base import ReportBase
from app.reports.student_performance import StudentPerformanceReport
from app.reports.teacher_performance import TeacherPerformanceReport
from app.reports.subject_performance import SubjectPerformanceReport


class DummyDataStore:
    def __init__(self, averages):
        self.averages = averages

    def get_student_averages(self):
        return dict(self.averages)


def normalize_table_str(s: str) -> str:
    return "\n".join(line.rstrip() for line in s.strip().splitlines())


@pytest.fixture
def sample_student_ds():
    return DummyDataStore({
        "Alice": 5.0,
        "Bob": 4.0,
        "Charlie": 5.0,
        "Dave": 3.0,
    })


@pytest.mark.parametrize(
    "ds, expected, extra, expectation ",
    [
        (DummyDataStore({"Alice": 5.0,"Bob": 4.0,"Charlie": 5.0,"Dave": 3.0}),
        [("Alice", 5.0), ("Charlie", 5.0), ("Bob", 4.0), ("Dave", 3.0)],
        {"precision":2}, 
        does_not_raise()),
        (DummyDataStore({"Alice": 5.0,"Bob": 4.0,"Charlie": 5.0,"Dave": 3.0}),
         [("Alice", 5.0),("Charlie",5.0)],
         {"top":2}, 
        does_not_raise())
        
    ]
)
def test_student_build(ds, expected, extra, expectation):
    with expectation:
        rpt = StudentPerformanceReport(ds, **extra )
        rpt.build()
        assert rpt._rows == expected


def test_student_render_precision():
    ds = DummyDataStore({"Alice":5.0,"Bob":4.0})
    rpt = StudentPerformanceReport(ds, precision=1)
    rpt.build()
    rendered = rpt.render()
    headers = ("Student", "Average")
    table = [ ("Alice", f"{5.0:.1f}"),("Bob", f"{4.0:.1f}")]
    expected = tabulate(table, headers=headers, tablefmt="github", stralign="left", numalign="right")
    assert normalize_table_str(rendered) == normalize_table_str(expected)


def test_student_render_empty():
    ds = DummyDataStore({})
    rpt = StudentPerformanceReport(ds)
    rpt.build()
    rendered = rpt.render()
    assert "Student" in rendered and "Average" in rendered
    assert "Alice" not in rendered


@pytest.mark.parametrize(
    "extra",
    [
        {"one": 1, "2":"2"}, 
        {"2":"2"},
        {"precision":2 , "top":5},
        {"precision":2 , "top":5,"one": 1, "2":"2"},
        {"":""},
        {}
    ]
)
def test_report_factory_kwargs_passed(monkeypatch, datastore, extra):
    called = {}
    def fake_ctor(ds, **kwargs):
        called['datastore'] = ds
        called['kwargs'] = kwargs
        class Dummy(ReportBase):
            name = "dummy"
            def __init__(self, ds, **kwargs):
                super().__init__(ds)
            def build(self):pass
            def render(self):pass
        return Dummy(ds)

    ReportFactory._registry['dummy'] = fake_ctor  
    registry_name = "_registry"
    try:
        ReportFactory.create('dummy', datastore, **extra)
        assert called['datastore'] is datastore
        assert called['kwargs'] == {**extra}
    finally:
        getattr(ReportFactory, registry_name).pop('dummy', None)  

       
@pytest.mark.parametrize(
    "name, expectation", 
    [
    ("non-existent-report", pytest.raises(ReportError)),
    (StudentPerformanceReport.name, does_not_raise()),
    (TeacherPerformanceReport.name, does_not_raise()),
    (SubjectPerformanceReport.name, does_not_raise()),
    ]
)
def test_report_factory_positive_negative(name, expectation, datastore):
    with expectation:
        r = ReportFactory.create(name, datastore)
        assert isinstance(r, ReportBase)

        
@pytest.mark.parametrize(
    "performance, expectation",
    [
        (StudentPerformanceReport, does_not_raise()),
        (TeacherPerformanceReport, does_not_raise()),
        (SubjectPerformanceReport, does_not_raise()),
        ("non-existent-report", pytest.raises(AttributeError))
    ]
)      
def test_report_factory_registered_reports(performance, expectation, datastore):
    with expectation:
        regist = ReportFactory.create(performance.name, datastore)
        assert isinstance(regist, ReportBase) and isinstance(regist, performance)


@pytest.mark.parametrize(
    "registered_ctor, expect_instance, expect_isinstance",
    [
        # позитивный случай: ctor возвращает инстанс ReportBase (должен пройти isinstance)
        (
            lambda ds, **kwargs: _make_dummy_instance(ds, implement_build=True),
            True,
            True,
        ),
        # негативный случай: ctor возвращает что-то не-наследующее ReportBase (isinstance -> False)
        (
            lambda datastore, **kwargs: object(),
            True,
            False,
        ),
    ],
)
def test_create_and_isinstance(datastore, registered_ctor, expect_instance, expect_isinstance):
    ReportFactory._registry['dummy'] = registered_ctor  # type: ignore
    r = ReportFactory.create('dummy', datastore, opt1=1, opt2="x")
    assert (r is not None) == expect_instance
    assert isinstance(r, ReportBase) is expect_isinstance


def _make_dummy_instance(datastore, implement_build: bool):
    class Dummy(ReportBase):
        name = "dummy"
        if implement_build:
            def build(self):
                return None
        else:
            pass
        def render(self):
            return "rendered"
    if not implement_build:
        return object()
    return Dummy(datastore)