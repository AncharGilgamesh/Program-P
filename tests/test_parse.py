"""Проверки разбора плана. Запуск: uv run python tests/test_parse.py"""

import sys
import tempfile
from pathlib import Path

from docx import Document

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Models.datahandler import (  # noqa: E402
    count_directed_students,
    parse_fiveth_table,
    parse_practice_table,
    parse_second_table,
    parse_sixth_table,
    read_plan_from_docx,
)


def practice_row(group, dates, practice):
    row = [""] * 9
    row[0] = group
    row[1] = practice
    row[2] = dates
    row[7] = "09.03.02"
    return row


def test_fourth_course_semester():
    autumn = parse_practice_table(
        [practice_row("4411", "01.09.2025-30.09.2025", "Учебная практика")]
    )
    spring = parse_practice_table(
        [practice_row("4411", "01.02.2025-28.02.2025", "Производственная практика")]
    )
    assert autumn[0][3] == 7
    assert spring[0][3] == 8


def test_directed_students_ignore_year_in_title():
    text = "Учебная практика 2024\nГ/б - 10\nПл. - 2\nЦелевики - 1"
    assert count_directed_students(text) == 13
    row = [""] * 8
    row[0] = "4411"
    row[1] = text
    row[2] = "01.09.2025-30.09.2025"
    row[3] = "Кафедра"
    parsed = parse_second_table([row])
    assert parsed[0][3] == 13


def test_fiveth_table_skips_rows_without_group_code():
    rows = parse_second_table(
        [
            _second_row("2301", "цех без кода"),
            _second_row("4411", "Кафедра"),
        ]
    )
    parsed, skipped = parse_fiveth_table(rows)
    assert skipped == 1
    assert len(parsed) == 1
    assert parsed[0][0] == "4411"


def test_sixth_table_leaves_missing_teacher_empty():
    practices = [[1, "4411", "09.03.02", 7, "Учебная практика", ""]]
    without_teacher = parse_sixth_table(practices, [["шапка"]])
    assert without_teacher[0][1] == ""
    with_teacher = parse_sixth_table(
        practices, [["шапка"], ["", "", "", "", "", "Иванов И.И."]]
    )
    assert with_teacher[0][1] == "Иванов И.И."


def test_plan_without_group_code_does_not_raise():
    document = Document()
    table = document.add_table(rows=3, cols=9)
    data_row = table.rows[2]
    data_row.cells[0].text = "2301"
    data_row.cells[1].text = "Практика 2024\nГ/б - 4\nПл. - 1\nЦелевики - 0"
    data_row.cells[2].text = "01.09.2025-30.09.2025"
    data_row.cells[3].text = "цех"
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "plan.docx"
        document.save(path)
        loaded = read_plan_from_docx(str(path))
    practices = parse_practice_table(loaded[1:])
    places = parse_second_table(loaded[1:])
    grades, skipped = parse_fiveth_table(places)
    teachers = parse_sixth_table(practices, loaded)
    assert practices[0][3] == 5
    assert places[0][3] == 5
    assert skipped == 1
    assert grades == []
    assert teachers[0][1] == ""


def _second_row(group, place):
    row = [""] * 8
    row[0] = group
    row[1] = "Практика 2024\nГ/б - 4\nПл. - 0\nЦелевики - 0"
    row[2] = "01.09.2025"
    row[3] = place
    return row


def main():
    test_fourth_course_semester()
    test_directed_students_ignore_year_in_title()
    test_fiveth_table_skips_rows_without_group_code()
    test_sixth_table_leaves_missing_teacher_empty()
    test_plan_without_group_code_does_not_raise()
    print("parse-checks-ok")


if __name__ == "__main__":
    main()
