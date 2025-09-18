# Тесты для app.datastore.DataStore
# Проверяем:
# - корректное накопление оценок по студентам, предметам и преподавателям
# - вычисление средних значений
# - top_n сортировку и ограничение по n
# - поведение при пустых данных
#
# Запуск
# pytest -v tests/test_datastore.py
import pytest

from tests.conftest import datastore, populated_datastore


def test_empty_datastore_behaviour(datastore):
    assert datastore.get_student_averages() == {}
    assert datastore.get_teacher_averages() == {}
    assert datastore.get_subject_averages() == {}
    assert datastore.top_n({}, n=5) == []
    

def test_get_student_averages(populated_datastore):
    ds = populated_datastore
    students = ds.get_student_averages()
    assert pytest.approx(students["Ivan"], rel=1e-6) == 4.5
    assert pytest.approx(students["Olga"], rel=1e-6) == 4.0
    
    
def test_get_teacher_averages(populated_datastore):
    ds = populated_datastore
    teachers = ds.get_teacher_averages()
    assert pytest.approx(teachers["Petrov"], rel=1e-6) == 4.5
    assert pytest.approx(teachers["Ivanov"], rel=1e-6) == 4.0


def test_get_subject_averages(populated_datastore):
    ds = populated_datastore
    subjects = ds.get_subject_averages()
    assert pytest.approx(subjects["Math"], rel=1e-6) == 4.5
    assert pytest.approx(subjects["Chem"], rel=1e-6) == 4.0


def test_top_n_ordering_and_limit(populated_datastore):
    ds = populated_datastore
    student_avgs = ds.get_student_averages()
    top2 = ds.top_n(student_avgs, n=2)
    assert top2[0][0] == "Ivan"
    assert pytest.approx(top2[0][1]) == 4.5
    assert len(top2) == 2
