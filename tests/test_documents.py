"""Срок хранения и имена файлов. Запуск: uv run python tests/test_documents.py"""

import datetime
import sys
import tempfile
from pathlib import Path

from docx import Document

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Models.datahandler import rows_from_saved_report
from main import saves_filename, split_expired_documents
from window_support import path_inside_saves


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


def test_saved_report_reads_six_tables_without_the_template():
    document = Document()
    for index in range(6):
        table = document.add_table(rows=2 if index == 0 else 1, cols=2)
        if index == 0:
            table.rows[1].cells[0].text = "4411"
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "report.docx"
        document.save(path)
        loaded_doc = Document(path)
    tables = rows_from_saved_report(loaded_doc, (1, 2, 2, 2, 4, 2), (6, 7, 3, 8, 8, 8))
    assert len(tables) == 6
    assert len(tables[0]) == 1
    assert tables[0][0] == ["4411", "", "", "", "", ""]
    assert tables[1:] == [[], [], [], [], []]


def test_path_must_stay_inside_saves():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        saves = root / "Saves"
        saves.mkdir()
        inside = saves / "plan.docx"
        inside.write_bytes(b"x")
        outside = root / "window_support.py"
        outside.write_bytes(b"x")
        assert path_inside_saves(inside, root) is True
        assert path_inside_saves("Saves/../window_support.py", root) is False
        assert path_inside_saves(outside, root) is False
        assert path_inside_saves("", root) is False


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
    test_saved_report_reads_six_tables_without_the_template()
    test_path_must_stay_inside_saves()
    test_saves_names_differ_within_one_day()
    print("document-checks-ok")


if __name__ == "__main__":
    main()
