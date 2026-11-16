import datetime
import sqlite3
import sys
import tempfile
from pathlib import Path

from docx import Document

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import window_support
from Models.datahandler import rows_from_saved_report
from View.report_page import report_replace_needs_confirm
from main import saves_filename, split_expired_documents
from window_support import locate_saved_file, path_inside_saves, release_saved_copy, save_registered_copy


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


def test_saved_report_drops_header_rows_before_the_start_index():
    starts = (1, 2, 2, 2, 4, 2)
    widths = (6, 7, 3, 8, 8, 8)
    document = Document()
    for start, width in zip(starts, widths):
        table = document.add_table(rows=start + 1, cols=width)
        for header_index in range(start):
            table.rows[header_index].cells[0].text = f"шапка {header_index}"
        table.rows[start].cells[0].text = "данные"
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "report.docx"
        document.save(path)
        loaded = Document(path)
    tables = rows_from_saved_report(loaded, starts, widths)
    assert len(tables) == 6
    for rows in tables:
        assert len(rows) == 1
        joined = " ".join(rows[0])
        assert "данные" in joined
        assert "шапка" not in joined


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


def test_locate_saved_file_follows_the_folder():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        saves = root / "Saves"
        saves.mkdir()
        plan = saves / "plan.docx"
        plan.write_bytes(b"x")
        (root / "window_support.py").write_bytes(b"y")
        (saves / "window_support.py").write_bytes(b"no")
        assert locate_saved_file("Saves/plan.docx", root) == plan.resolve()
        assert locate_saved_file("Saves/../window_support.py", root) is None
        assert locate_saved_file("", root) is None
        assert locate_saved_file(str(plan), root) == plan.resolve()
        old = root / "old_copy" / "Saves" / "plan.docx"
        assert locate_saved_file(str(old), root) == plan.resolve()
        missing = root / "old_copy" / "Saves" / "absent.docx"
        assert locate_saved_file(str(missing), root) is None
        outside = root / "notes.docx"
        outside.write_bytes(b"z")
        assert locate_saved_file(str(outside), root) is None


def test_save_writes_a_relative_saves_path():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        captured = {}
        original_base = window_support.base_dir
        original_insert = window_support.dbh.insert_document

        def insert_document(*args):
            captured["args"] = args

        class Doc:
            def save(self, path):
                Path(path).write_bytes(b"doc")

        class Window:
            user = "user"

        window_support.base_dir = str(root)
        window_support.dbh.insert_document = insert_document
        try:
            save_registered_copy(Window(), Doc(), "План")
        finally:
            window_support.base_dir = original_base
            window_support.dbh.insert_document = original_insert
        stored = captured["args"][4]
        assert stored.startswith("Saves/")
        assert not Path(stored).is_absolute()
        assert (root / stored).is_file()


def test_failed_insert_removes_the_new_file():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        original_base = window_support.base_dir
        original_insert = window_support.dbh.insert_document
        original_warning = window_support.QMessageBox.warning

        def insert_document(*args):
            raise sqlite3.Error("insert failed")

        window_support.base_dir = str(root)
        window_support.dbh.insert_document = insert_document
        window_support.QMessageBox.warning = lambda *args, **kwargs: None

        class Doc:
            def save(self, path):
                Path(path).write_bytes(b"doc")

        class Window:
            user = "user"

        try:
            save_registered_copy(Window(), Doc(), "План")
        finally:
            window_support.base_dir = original_base
            window_support.dbh.insert_document = original_insert
            window_support.QMessageBox.warning = original_warning
        assert list((root / "Saves").glob("*")) == []


def test_failed_file_delete_keeps_the_row():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        saves = root / "Saves"
        saves.mkdir()
        target = saves / "plan.docx"
        target.write_bytes(b"doc")
        original_remove = window_support.os.remove

        def refuse_remove(path):
            raise OSError("busy")

        window_support.os.remove = refuse_remove
        removed = []
        try:
            status, detail = release_saved_copy("Saves/plan.docx", root)
            if status == "ready":
                removed.append(1)
        finally:
            window_support.os.remove = original_remove
        assert status == "kept"
        assert detail == "busy"
        assert removed == []
        assert target.is_file()


def test_report_replace_needs_confirm_when_any_table_has_rows():
    assert report_replace_needs_confirm((0, 0, 0, 0, 0, 0)) is False
    assert report_replace_needs_confirm((0, 0, 1, 0, 0, 0)) is True


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
    test_saved_report_drops_header_rows_before_the_start_index()
    test_path_must_stay_inside_saves()
    test_locate_saved_file_follows_the_folder()
    test_save_writes_a_relative_saves_path()
    test_failed_insert_removes_the_new_file()
    test_failed_file_delete_keeps_the_row()
    test_report_replace_needs_confirm_when_any_table_has_rows()
    test_saves_names_differ_within_one_day()
    print("document-checks-ok")


if __name__ == "__main__":
    main()
