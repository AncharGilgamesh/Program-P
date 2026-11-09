"""Учебные Excel и Word в этой папке. Запуск: uv run python Example/build_examples.py"""

import sys
from pathlib import Path

import pandas as pd
from docx import Document

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Models.datahandler import (  # noqa: E402
    apply_student_block,
    choose_student_block,
    extract_additional_info_form_nagruzka,
    extract_practice_blocks_with_empty_stop,
    parse_fiveth_table,
    parse_fourth_table,
    parse_practice_table,
    parse_second_table,
    parse_sixth_table,
    parse_third_table,
    read_plan_from_docx,
    transform_practice_data,
)
from Models.docx_writer import fill_the_table_rows  # noqa: E402
from window_support import OTCHET_TABLE_START_ROWS, shablon_otch_path, shablon_plan_path  # noqa: E402

OUT = Path(__file__).resolve().parent
TABLE_NAME = "таблица_практик.xlsx"
WORKLOAD_NAME = "нагрузка.xlsx"
PLAN_NAME = "план.docx"
REPORT_NAME = "отчёт.docx"
WORKLOAD_WIDTH = 30


def practice_sheet_rows(blocks):
    """Лист кафедральной таблицы: заголовок блока, шапка, строки групп."""
    rows = []
    for title, groups in blocks:
        rows.append([title, None, None, None, None])
        rows.append(["№", "Группа", "Преподаватель", "Направление", "Срок"])
        for group in groups:
            rows.append(list(group))
    return rows


def bachelor_sheet():
    return practice_sheet_rows(
        [
            (
                "Учебная практика – ознакомительная",
                [(1, "4111", "Иванов Иван Иванович", "09.03.02", "01.09.2025-30.09.2025")],
            ),
            (
                "Производственная практика – эксплуатационная",
                [(2, "4211", "Петров Пётр Петрович", "09.03.02", "02.02.2026-28.02.2026")],
            ),
        ]
    )


def master_sheet():
    return practice_sheet_rows(
        [
            (
                "Производственная практика: Научно-исследовательская работа",
                [(1, "4411", "Сидоров Сидор Сидорович", "09.04.02", "01.09.2025-30.09.2025")],
            )
        ]
    )


def workload_row(group, budget, paid, total, level, practice, period, teacher, specialty, note):
    row = [None] * WORKLOAD_WIDTH
    row[4] = group
    row[5] = budget
    row[6] = paid
    row[7] = total
    row[8] = specialty
    row[10] = level
    row[12] = practice
    row[13] = period
    row[16] = teacher
    row[29] = note
    return row


def workload_rows():
    header = [None] * WORKLOAD_WIDTH
    header[4] = "Группа"
    header[5] = "Бюджет"
    header[6] = "Платное"
    header[7] = "Всего"
    header[8] = "Специальность"
    header[10] = "Уровень"
    header[12] = "Вид практики"
    header[13] = "Срок"
    header[16] = "Руководитель"
    header[29] = "Примечание"
    return [
        header,
        workload_row(
            "4111",
            10,
            2,
            13,
            "бакалавриат",
            "Учебная практика – ознакомительная",
            "01.09.2025-30.09.2025",
            "Иванов Иван Иванович",
            "09.03.02 Информатика и вычислительная техника",
            "пример",
        ),
        workload_row(
            "4211",
            8,
            0,
            8,
            "бакалавриат",
            "Производственная практика – эксплуатационная",
            "02.02.2026-28.02.2026",
            "Петров Пётр Петрович",
            "09.03.02 Информатика и вычислительная техника",
            "пример",
        ),
        workload_row(
            "4411",
            5,
            1,
            6,
            "магистратура",
            "Производственная практика: Научно-исследовательская работа",
            "01.09.2025-30.09.2025",
            "Сидоров Сидор Сидорович",
            "09.04.02 Информационные системы и технологии",
            "пример",
        ),
    ]


def plan_rows_from_files(table_path, workload_path):
    """Те же шаги, что «Загрузить таблицу», затем «Загрузить нагрузку»."""
    with pd.ExcelFile(table_path) as book:
        bachelor = pd.read_excel(book, 0, header=None)
        master = pd.read_excel(book, 1, header=None)
    bachelor_rows = transform_practice_data(extract_practice_blocks_with_empty_stop(bachelor))
    master_rows = transform_practice_data(
        extract_practice_blocks_with_empty_stop(master), len(bachelor_rows)
    )
    rows = bachelor_rows + master_rows
    workload = pd.read_excel(workload_path, header=None)
    blocks = extract_additional_info_form_nagruzka(workload)
    for row in rows:
        block = choose_student_block(blocks, row[1], row[2])
        if block is not None:
            row[2] = apply_student_block(row[2], block)
    return rows


def write_plan(rows, path):
    document = Document(shablon_plan_path)
    fill_the_table_rows(document.tables[0], [row[1:] for row in rows], 2)
    document.save(path)


def write_report(plan_path, path):
    """Те же шесть таблиц, что «Загрузить план» на странице отчёта."""
    body = read_plan_from_docx(plan_path)[1:]
    tables = [
        parse_practice_table(body),
        parse_second_table(body),
        parse_third_table(body),
        parse_fourth_table(parse_second_table(body)),
        parse_fiveth_table(parse_second_table(body))[0],
        parse_sixth_table(body),
    ]
    document = Document(shablon_otch_path)
    for table, data, start_row in zip(document.tables, tables, OTCHET_TABLE_START_ROWS):
        fill_the_table_rows(table, data, start_row)
    document.save(path)


def main():
    table_path = OUT / TABLE_NAME
    workload_path = OUT / WORKLOAD_NAME
    plan_path = OUT / PLAN_NAME
    report_path = OUT / REPORT_NAME
    with pd.ExcelWriter(table_path, engine="openpyxl") as writer:
        pd.DataFrame(bachelor_sheet()).to_excel(
            writer, sheet_name="Бакалавриат", header=False, index=False
        )
        pd.DataFrame(master_sheet()).to_excel(
            writer, sheet_name="Магистратура", header=False, index=False
        )
    pd.DataFrame(workload_rows()).to_excel(workload_path, header=False, index=False)
    rows = plan_rows_from_files(table_path, workload_path)
    if [row[1] for row in rows] != ["4111", "4211", "4411"]:
        raise SystemExit(f"неожиданные группы: {[row[1] for row in rows]}")
    if "Г/б - 10" not in rows[0][2] or "Г/б - 8" not in rows[1][2] or "Г/б - 5" not in rows[2][2]:
        raise SystemExit("нагрузка не дописала числа студентов")
    write_plan(rows, plan_path)
    write_report(plan_path, report_path)
    print(table_path)
    print(workload_path)
    print(plan_path)
    print(report_path)


if __name__ == "__main__":
    main()
