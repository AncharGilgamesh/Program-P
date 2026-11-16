import pytest
from PySide6.QtCore import Qt

from Models.model import PlanTableModel, ResultTableModel

pytestmark = pytest.mark.usefixtures("qapp")

HEADERS = [
    "Группа",
    "Всего",
    "Отл.",
    "Хор.",
    "Удовл.",
    "Неуд.",
    "Не защитило",
    "Место",
]


def grade_row():
    return ["4411", "10", "4", "3", "2", "0", "", "в КНИТУ-КАИ"]


def test_locked_directory_model_rejects_edits():
    model = PlanTableModel([("1", "Иванов")], ["id", "Фамилия"], editable=False)
    index = model.index(0, 1)
    assert not (model.flags(index) & Qt.ItemIsEditable)
    assert model.setData(index, "Петров", Qt.EditRole) is False
    assert model.data(index, Qt.DisplayRole) == "Иванов"


def test_undefended_is_total_minus_scores():
    model = ResultTableModel([grade_row()], HEADERS)
    assert model.data(model.index(0, 6), Qt.DisplayRole) == "1"


def test_score_sum_cannot_exceed_total():
    model = ResultTableModel([grade_row()], HEADERS)
    excellent = model.index(0, 2)
    assert model.setData(excellent, "6", Qt.EditRole) is False
    assert model.data(excellent, Qt.DisplayRole) == "4"
    assert model.data(model.index(0, 6), Qt.DisplayRole) == "1"


def test_total_cannot_drop_below_recorded_scores():
    model = ResultTableModel([grade_row()], HEADERS)
    total = model.index(0, 1)
    assert model.setData(total, "8", Qt.EditRole) is False
    assert model.data(total, Qt.DisplayRole) == "10"


def test_undefended_column_is_read_only():
    model = ResultTableModel([grade_row()], HEADERS)
    undefended = model.index(0, 6)
    assert not (model.flags(undefended) & Qt.ItemIsEditable)
    assert model.setData(undefended, "0", Qt.EditRole) is False
    assert model.data(undefended, Qt.DisplayRole) == "1"


def test_accepted_score_updates_undefended():
    model = ResultTableModel([grade_row()], HEADERS)
    assert model.setData(model.index(0, 5), "1", Qt.EditRole) is True
    assert model.data(model.index(0, 6), Qt.DisplayRole) == "0"
