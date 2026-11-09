"""Срок хранения и имена файлов. Запуск: uv run python tests/test_documents.py"""

import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from main import saves_filename, split_expired_documents


def row(created, protected, doc_type="План"):
    return [1, 2020, doc_type, created, "user", protected, "Saves/file.docx"]


def test_five_year_split():
    today = datetime.date(2026, 11, 9)
    rows = [
        row("2021.11.09", 0),
        row("2021.11.10", 0),
        row("2020.01.01", 1, "Отчет"),
        row("2024.06.01", 0),
        row("не дата", 0),
    ]
    expired, protected = split_expired_documents(rows, today)
    assert [item[3] for item in expired] == ["2021.11.09"]
    assert [item[3] for item in protected] == ["2020.01.01"]


def test_report_tables_share_one_start_row_scheme():
    from main import OTCHET_TABLE_START_ROWS

    assert OTCHET_TABLE_START_ROWS == (1, 2, 2, 2, 4, 2)


def test_saves_names_differ_within_one_day():
    morning = datetime.datetime(2026, 11, 9, 10, 0, 0)
    evening = datetime.datetime(2026, 11, 9, 18, 30, 1)
    plan_a = saves_filename(2026, "План", morning)
    plan_b = saves_filename(2026, "План", evening)
    report = saves_filename(2026, "Отчет", morning)
    assert plan_a != plan_b
    assert plan_a.startswith("2026_p_")
    assert report.startswith("2026_o_")
    assert "20261109" in plan_a and "20261109" in plan_b


def main():
    test_five_year_split()
    test_report_tables_share_one_start_row_scheme()
    test_saves_names_differ_within_one_day()
    print("document-checks-ok")


if __name__ == "__main__":
    main()
