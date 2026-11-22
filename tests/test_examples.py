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
GROUPS = ["4111", "4112", "4211", "4311", "4411", "4151", "4251"]
INTRO = "Учебная практика – ознакомительная"


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
    assert [row[1] for row in rows] == GROUPS
    assert rows[0][8].startswith("01.03.02")
    assert rows[5][8].startswith("01.04.02")
    assert rows[0][4] == "Кафедра"
    assert INTRO in rows[0][2]
    assert "преддипломная" in rows[4][2]


def test_example_nagruzka():
    workload = pd.read_excel(EXAMPLE / "нагрузка.xlsx", header=None)
    blocks = extract_additional_info_form_nagruzka(workload)
    intro = blocks[("4111", INTRO)]
    assert "Г/б - 17" in intro
    assert "Пл. - 3" in intro
    assert "Целевики - 1" in intro
    diploma = "производственная практика – преддипломная"
    assert "Г/б - 13" in blocks[("4411", diploma)]
    built = extract_data(workload)
    assert [row[1] for row in built] == GROUPS
    assert built[4][1] == "4411"
    assert built[5][8] == "01.04.02"


def test_example_docx():
    plan = rows_from_saved_plan(read_plan_from_docx(EXAMPLE / "план.docx"))
    assert [row[1] for row in plan] == GROUPS
    assert "Г/б - 17" in plan[0][2]
    assert plan[0][4] == "Кафедра"
    assert "АйСиЭл" in plan[3][4]
    assert plan[3][5] == "103-П/2025"
    report = Document(EXAMPLE / "отчёт.docx")
    tables = rows_from_saved_report(report, OTCHET_TABLE_START_ROWS, (6, 7, 3, 8, 8, 8))
    assert [row[1] for row in tables[0]] == GROUPS
    assert [row[3] for row in tables[0]] == ["1", "1", "4", "6", "8", "1", "4"]
    assert tables[1][0][3] == tables[1][0][4] == "21"
    assert tables[4][0][5] == "1"
    assert tables[4][2][6] == "1"
    assert len(tables) == 6
    assert all(tables)
