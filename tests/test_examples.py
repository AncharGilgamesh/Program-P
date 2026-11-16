import sys
from pathlib import Path

import pandas as pd
from docx import Document

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Models.datahandler import (  # noqa: E402
    extract_additional_info_form_nagruzka,
    extract_data,
    extract_practice_blocks_with_empty_stop,
    rows_from_saved_plan,
    rows_from_saved_report,
    read_plan_from_docx,
    transform_practice_data,
)
from window_support import OTCHET_TABLE_START_ROWS  # noqa: E402

EXAMPLE = Path(__file__).resolve().parents[1] / "Example"


def _plan_rows():
    table = EXAMPLE / "таблица_практик.xlsx"
    with pd.ExcelFile(table) as book:
        bachelor = pd.read_excel(book, 0, header=None)
        master = pd.read_excel(book, 1, header=None)
    bachelor_rows = transform_practice_data(extract_practice_blocks_with_empty_stop(bachelor))
    master_rows = transform_practice_data(
        extract_practice_blocks_with_empty_stop(master), len(bachelor_rows)
    )
    return bachelor_rows + master_rows


def test_example_groups():
    rows = _plan_rows()
    assert [row[1] for row in rows] == ["4111", "4211", "4411"]
    assert rows[0][8] == "09.03.02"
    assert rows[0][4] == "Кафедра"


def test_example_nagruzka():
    workload = pd.read_excel(EXAMPLE / "нагрузка.xlsx", header=None)
    blocks = extract_additional_info_form_nagruzka(workload)
    assert "Г/б - 10" in blocks[("4111", "Учебная практика – ознакомительная")]
    assert "Целевики - 1" in blocks[("4111", "Учебная практика – ознакомительная")]
    built = extract_data(workload)
    assert [row[1] for row in built] == ["4111", "4211", "4411"]
    assert built[2][1] == "4411"


def test_example_docx():
    plan = rows_from_saved_plan(read_plan_from_docx(EXAMPLE / "план.docx"))
    assert [row[1] for row in plan] == ["4111", "4211", "4411"]
    assert "Г/б - 10" in plan[0][2]
    report = Document(EXAMPLE / "отчёт.docx")
    tables = rows_from_saved_report(report, OTCHET_TABLE_START_ROWS, (6, 7, 3, 8, 8, 8))
    assert [row[1] for row in tables[0]] == ["4111", "4211", "4411"]
    assert len(tables) == 6
    assert all(tables)
