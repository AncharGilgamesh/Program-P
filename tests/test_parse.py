"""Проверки разбора плана. Запуск: uv run python tests/test_parse.py"""

import sys
import tempfile
from pathlib import Path

import pandas as pd
import pytest
from docx import Document

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Models.datahandler import (  # noqa: E402
    apply_student_block,
    choose_student_block,
    count_directed_students,
    extract_additional_info_form_nagruzka,
    extract_data,
    transform_practice_data,
    extract_first_month,
    extract_meeting_date,
    extract_start_end_dates,
    normalize_group,
    normalize_practice_period,
    parse_workload_teacher,
    normalize_practice_type,
    parse_fiveth_table,
    parse_practice_table,
    parse_third_table,
    parse_second_table,
    parse_sixth_table,
    read_plan_from_docx,
)
from View.plan_page import plan_replace_needs_confirm  # noqa: E402


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
    empty = practice_row("4411", "01.09.2025-30.09.2025", "Учебная практика")
    filled = practice_row("4411", "01.09.2025-30.09.2025", "Учебная практика")
    filled[5] = "Иванов И.И."
    assert parse_sixth_table([empty])[0][1] == ""
    assert parse_sixth_table([filled])[0][1] == "Иванов И.И."


def test_short_row_does_not_shift_following_teacher():
    first = practice_row("4411", "01.09.2025-30.09.2025", "Учебная практика")
    first[5] = "Иванов И.И."
    second = practice_row("4412", "01.02.2025-28.02.2025", "Производственная практика")
    second[5] = "Петров П.П."
    parsed = parse_sixth_table([first, ["короткая"], second])
    assert [row[0] for row in parsed] == ["1", "2"]
    assert [row[3] for row in parsed] == ["4411", "4412"]
    assert [row[1] for row in parsed] == ["Иванов И.И.", "Петров П.П."]


def test_excel_date_becomes_first_of_september():
    assert normalize_practice_period(pd.Timestamp("2025-09-01")) == "01.09.2025"
    assert normalize_practice_period("2025-09-01 00:00:00") == "01.09.2025"
    assert extract_first_month("2025-09-01 00:00:00") == 9
    assert extract_meeting_date("2025-09-01 00:00:00") == "01.09.2025"
    parsed = parse_practice_table(
        [practice_row("4411", "2025-09-01 00:00:00", "Учебная практика")]
    )
    assert parsed[0][3] == 7
    assert parsed[0][5] == "01.09.2025"
    start, end = extract_start_end_dates("01.09.2025-30.09.2025")
    assert (start, end) == ("01.09.2025", "30.09.2025")
    autumn = parse_practice_table(
        [practice_row("4411", "01.09.2025-30.09.2025", "Учебная практика")]
    )
    assert autumn[0][3] == 7
    width = 30
    row = [None] * width
    row[4] = 4411
    row[10] = "бакалавриат"
    row[13] = pd.Timestamp("2025-09-01")
    loaded = extract_data(pd.DataFrame([[None] * width, row]))
    assert loaded[0][3] == "01.09.2025"


def test_unknown_practice_title_survives_in_the_report():
    diploma = "Преддипломная практика\nГ/б - 4\nПл. - 0\nЦелевики - 0"
    row = practice_row("4411", "01.09.2025-30.09.2025", diploma)
    assert parse_practice_table([row])[0][4] == "Преддипломная практика"
    assert parse_sixth_table([row])[0][4] == "Преддипломная практика"
    known = "Учебная практика – ознакомительная\nГ/б - 1\nПл. - 0\nЦелевики - 0"
    known_row = practice_row("4411", "01.09.2025-30.09.2025", known)
    assert parse_practice_table([known_row])[0][4].startswith("Учебная практика")
    assert parse_sixth_table([known_row])[0][4].startswith("Учебная практика")


def test_third_table_lists_groups_in_sorted_order():
    rows = [
        ["4412", "", "", "цех", "", "Иванов И.И."],
        ["4411", "", "", "цех", "", "Иванов И.И."],
    ]
    parsed = parse_third_table(rows)
    assert len(parsed) == 1
    place = parsed[0][0]
    assert place.index("4411") < place.index("4412")


def test_unreadable_date_leaves_semester_empty():
    parsed = parse_practice_table([practice_row("4411", "без даты", "Учебная практика")])
    assert parsed[0][3] == ""
    assert parse_practice_table([["4411", "короткая строка"]]) == []


def test_short_and_broken_report_rows_do_not_raise():
    parsed, skipped = parse_fiveth_table(
        [["короткая"], ["", "", "нет кода"], ["", "", "гр. 4411", "12"]]
    )
    assert skipped == 2
    assert parsed == [["4411", "12", "", "", "", "", "", "в КНИТУ-КАИ"]]
    assert parse_sixth_table([["короткая"]]) == []


def test_apply_student_block_replaces_numbers_and_keeps_year():
    title = "Учебная практика 2024"
    first = apply_student_block(title, "\nГ/б - 10\nПл. - 2\nЦелевики - 1")
    assert first == "Учебная практика 2024\nГ/б - 10\nПл. - 2\nЦелевики - 1"
    second = apply_student_block(first, "Г/б - 3\nПл. - 1\nЦелевики - 0")
    assert "2024" in second
    assert second.count("Г/б") == 1
    assert "Г/б - 10" not in second
    assert second.endswith("Г/б - 3\nПл. - 1\nЦелевики - 0")


def _workload_row(group):
    row = [None] * 30
    row[4] = group
    row[10] = "бакалавриат"
    return row


def test_workload_group_drops_decimal_tail():
    loaded = extract_data(pd.DataFrame([[None] * 30, _workload_row(4411.0), _workload_row("4411.0")]))
    assert [row[1] for row in loaded] == ["4411", "4411"]
    transformed = transform_practice_data(
        [
            {
                "title": "Учебная практика",
                "data": [
                    ["шапка", "группа", "фио", "направление", "сроки"],
                    ["", 4311.0, "Иванов", "09.03.02", "01.09.2025"],
                ],
            }
        ]
    )
    assert transformed[0][1] == "4311"


def test_workload_teacher_keeps_initials_and_full_name():
    assert parse_workload_teacher("иванов и.и.") == "Иванов И.И."
    assert parse_workload_teacher("Иванов И.И.") == "Иванов И.И."
    assert parse_workload_teacher("Иванов И. И.") == "Иванов И.И."
    assert parse_workload_teacher("Иванов Иван Иванович") == "Иванов Иван Иванович"
    assert parse_workload_teacher("") == ""
    assert parse_workload_teacher(None) == ""
    assert parse_workload_teacher("-") == ""


def test_empty_total_keeps_zero_targeted():
    row = [None] * 8
    row[4] = "4411"
    row[5] = 10
    row[6] = 2
    block = extract_additional_info_form_nagruzka(pd.DataFrame([[None] * 8, row]))[("4411", "")]
    assert "Г/б - 10" in block
    assert "Пл. - 2" in block
    assert "Целевики - 0" in block


def test_total_below_budget_and_paid_names_the_group():
    row = [None] * 8
    row[4] = 4411
    row[5] = 8
    row[6] = 5
    row[7] = 10
    with pytest.raises(ValueError, match="4411"):
        extract_additional_info_form_nagruzka(pd.DataFrame([[None] * 8, row]))


def test_group_keys_match_after_normalization():
    assert normalize_group(4111) == normalize_group("4111") == normalize_group("4111.0") == "4111"


def _nagruzka_frame(rows):
    width = 13 if any(len(item) > 2 for item in rows) else 8
    header = [None] * width
    body = []
    for item in rows:
        group, budget = item[0], item[1]
        practice = item[2] if len(item) > 2 else None
        row = [None] * width
        row[4] = group
        row[5] = budget
        if width > 12:
            row[12] = practice
        body.append(row)
    return pd.DataFrame([header, *body])


def test_repeated_group_counts_are_summed():
    same = extract_additional_info_form_nagruzka(_nagruzka_frame([(4411, 10), (4411, 3)]))
    assert list(same) == [("4411", "")]
    assert same[("4411", "")].count("Г/б") == 1
    assert "Г/б - 13" in same[("4411", "")]

    merged = extract_additional_info_form_nagruzka(_nagruzka_frame([(4111, 10), ("4111.0", 3)]))
    assert list(merged) == [("4111", "")]
    assert "Г/б - 13" in merged[("4111", "")]
    assert "Г/б - 10" not in merged[("4111", "")]


def test_same_group_keeps_separate_practice_counts():
    result = extract_additional_info_form_nagruzka(
        _nagruzka_frame(
            [
                (4411, 10, "ознакомительная"),
                (4411, 4, "эксплуатационная"),
            ]
        )
    )
    intro = ("4411", normalize_practice_type("ознакомительная"))
    field = ("4411", normalize_practice_type("эксплуатационная"))
    assert set(result) == {intro, field}
    assert result[intro].count("Г/б") == 1
    assert "Г/б - 10" in result[intro]
    assert result[field].count("Г/б") == 1
    assert "Г/б - 4" in result[field]


def test_unrecognized_practice_gets_the_only_group_block():
    only = extract_additional_info_form_nagruzka(
        _nagruzka_frame([(4411, 10, "ознакомительная")])
    )
    block = choose_student_block(only, "4411", "Учебная практика")
    assert block == only[("4411", normalize_practice_type("ознакомительная"))]

    empty_kind = extract_additional_info_form_nagruzka(_nagruzka_frame([(4411, 7)]))
    assert "Г/б - 7" in choose_student_block(empty_kind, "4411", "Учебная практика")


def test_unrecognized_practice_stays_empty_when_group_has_two_kinds():
    both = extract_additional_info_form_nagruzka(
        _nagruzka_frame(
            [
                (4411, 10, "ознакомительная"),
                (4411, 4, "эксплуатационная"),
            ]
        )
    )
    assert choose_student_block(both, "4411", "Учебная практика") is None


def test_known_practice_word_selects_only_its_block():
    both = extract_additional_info_form_nagruzka(
        _nagruzka_frame(
            [
                (4411, 10, "ознакомительная"),
                (4411, 4, "эксплуатационная"),
            ]
        )
    )
    block = choose_student_block(both, "4411", "ознакомительная практика")
    assert block is not None
    assert "Г/б - 10" in block
    assert "Г/б - 4" not in block


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
    teachers = parse_sixth_table(loaded[1:])
    assert practices[0][3] == 5
    assert places[0][3] == 5
    assert skipped == 1
    assert grades == []
    assert teachers[0][1] == ""


def test_plan_replace_needs_confirm_only_for_a_filled_table():
    assert plan_replace_needs_confirm(0, True) is False
    assert plan_replace_needs_confirm(3, True) is True
    assert plan_replace_needs_confirm(3, False) is False


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
    test_short_row_does_not_shift_following_teacher()
    test_excel_date_becomes_first_of_september()
    test_unknown_practice_title_survives_in_the_report()
    test_third_table_lists_groups_in_sorted_order()
    test_unreadable_date_leaves_semester_empty()
    test_short_and_broken_report_rows_do_not_raise()
    test_apply_student_block_replaces_numbers_and_keeps_year()
    test_workload_group_drops_decimal_tail()
    test_workload_teacher_keeps_initials_and_full_name()
    test_empty_total_keeps_zero_targeted()
    test_total_below_budget_and_paid_names_the_group()
    test_plan_replace_needs_confirm_only_for_a_filled_table()
    test_group_keys_match_after_normalization()
    test_repeated_group_counts_are_summed()
    test_same_group_keeps_separate_practice_counts()
    test_unrecognized_practice_gets_the_only_group_block()
    test_unrecognized_practice_stays_empty_when_group_has_two_kinds()
    test_known_practice_word_selects_only_its_block()
    test_plan_without_group_code_does_not_raise()
    print("parse-checks-ok")


if __name__ == "__main__":
    main()
