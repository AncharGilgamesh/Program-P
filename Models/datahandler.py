import pandas as pd
import re
import sys
import os
from PySide6.QtCore import Qt
from docx import Document
from datetime import datetime
from collections import defaultdict
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt


# Для превращения относительного пути в абсолютный
def resource_path(relative_path):
    """Получение абсолютного пути к ресурсу для PyInstaller"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# Шестой этап
def parse_sixth_table(data, prepods):
    # data - table1
    # prepods - берем из общего плана
    result = []
    for i in range(0, len(data)):
        result.append(
            [str(i + 1), prepods[i + 1][5].strip(), "", data[i][1], data[i][4], "", "", ""]
        )
    return result


# Пятый этап отчета
def parse_fiveth_table(data):
    # i just wonder can i handle it
    # сюда передаю table2
    result = []
    for row in data:
        group = re.search(r"\b4\d{3}\b", row[2]).group()
        people_amount = row[3]
        result.append([group, people_amount, "", "", "", "", "", "в КНИТУ-КАИ"])
    return result


# Четвертый этап отчета
def parse_fourth_table(data):
    # сюда передаю table2
    result = []
    for row in data:
        result.append([row[2], "", "", "", "", "", "", "да"])
    return result


# Третий этап отчета


def parse_third_table(data_rows):
    result = []
    grouped = defaultdict(set)

    for row in data_rows:
        if len(row) < 6:
            continue

        group = row[0].strip()
        location = row[3].strip()
        teacher = row[5].strip()

        if "кафедра" in location.lower():
            final_place = "Учебная лаборатория кафедры ПМИ"
        else:
            final_place = f"{location}, Учебная каф. ПМИ"

        key = (final_place, teacher)
        grouped[key].add(group)

    for (place, teacher), groups in grouped.items():
        place_with_groups = f"{place}, " + ", ".join(groups)
        result.append([place_with_groups, teacher, ""])

    return result


# Второй этап отчета
def parse_second_table(data_rows):
    result = []

    for i, row in enumerate(data_rows):
        if len(row) < 8:
            continue  # пропускаем неполные строки

        group = row[0].strip()
        practice_text = row[1].strip()
        date_text = row[2].strip()
        place_text = row[3].strip()

        # 1. Нумерация
        number = i + 1

        # 2. Город
        city = "Казань"

        # 3. Место проведения
        if "кафедра" in place_text.lower():
            location = f"Учебная кафедра ПМИ, гр. {group}"
        elif place_text:
            location = f"{place_text}, Учебная каф. ПМИ, гр. {group}"
        else:
            location = f"Учебная каф. ПМИ, гр. {group}"

        # 4. Сколько человек направлено — ищем все числа в practice_text
        numbers = [int(n) for n in re.findall(r"\d+", practice_text)]
        people_count = sum(numbers)

        # 5. Пустая строка
        placeholder = ""

        # 6-7. Даты начала и конца практики
        start_date, end_date = extract_start_end_dates(date_text)

        result.append([number, city, location, people_count, placeholder, start_date, end_date])

    return result


def extract_start_end_dates(text):
    text = text.replace("\n", " ").replace("г.", "").replace("г", "").strip()
    date_matches = re.findall(r"(\d{1,2})[./-](\d{1,2})(?:[./-](\d{4}))?", text)

    if not date_matches:
        return "", ""

    # Первая дата
    day1, month1, *year1 = date_matches[0]
    day1 = int(day1)
    month1 = int(month1)
    year1 = int(year1[0]) if year1 and year1[0].isdigit() else None

    # Вторая дата (если есть)
    if len(date_matches) > 1:
        day2, month2, *year2 = date_matches[1]
        day2 = int(day2)
        month2 = int(month2)
        year2 = int(year2[0]) if year2 and year2[0].isdigit() else None
    else:
        day2 = month2 = year2 = None

    # Подставим год, если его нет у первой даты
    if not year1 and year2:
        year1 = year2
    elif not year1:
        year1 = datetime.now().year

    if not year2:
        year2 = year1

    try:
        start = datetime(day=day1, month=month1, year=year1).strftime("%d.%m.%Y")
    except Exception:
        start = ""

    try:
        end = (
            datetime(day=day2, month=month2, year=year2).strftime("%d.%m.%Y")
            if day2 and month2
            else ""
        )
    except Exception:
        end = ""

    return start, end


# Первый этап отчета
# Эта функция принимает данные из модели первого этапа отчета и разделяет группа - практика, для
# диалогового окна в дальнейшем
def get_group_practice_keys_frst_stg(data):
    seen = set()
    group_practice_list = []

    for row in data:
        if len(row) < 5:
            continue  # на всякий случай

        group = str(row[1]).strip()
        practice = str(row[4]).strip()

        # Сокращения
        practice_short = (
            practice.replace("по получению навыков научно-исследовательской работы", "ППНИР")
            .replace("научно-исследовательская работа", "НИР")
            .replace("научно-исследовательская  работа", "НИР")
        )

        key = f"{group} – {practice_short}"
        if key not in seen:
            seen.add(key)
            group_practice_list.append(key)

    return group_practice_list


def get_target_row_indices(data, selected_keys):
    """
    Возвращает список индексов строк, соответствующих выбранным ключам.
    Ключ: "Группа – Вид практики (с сокращением)"
    """
    target_indices = []

    for i, row in enumerate(data):
        if len(row) < 5:
            continue

        group = str(row[1]).strip()
        practice = str(row[4]).strip()

        # Сокращения
        practice_short = (
            practice.replace("по получению навыков научно-исследовательской работы", "ППНИР")
            .replace("научно-исследовательская работа", "НИР")
            .replace("научно-исследовательская  работа", "НИР")
        )

        key = f"{group} – {practice_short}"
        if key in selected_keys:
            target_indices.append(i)

    return target_indices


# Обработка плана для отчета
def parse_practice_table(data_rows):
    result = []

    for i, row in enumerate(data_rows):
        if len(row) < 9:
            continue  # пропускаем пустые строки

        group = row[0].strip()
        direction = row[7].strip()  # направление
        practice_text = row[1].strip()
        raw_dates = row[2].strip()

        # ===== 1. Семестр =====
        try:
            course_digit = int(str(group)[1])  # вторая цифра номера группы
        except (IndexError, ValueError):
            course_digit = None

        month = extract_first_month(raw_dates)
        semester = None
        if course_digit:
            if month and 1 <= month <= 6:
                semester = course_digit * 2
            elif month and 6 < month <= 12:
                semester = course_digit * 2 - 1

            # поправка для 8 семестра (второй семестр 4 курса)
            if semester == 7 and course_digit == 4:
                semester = 8

        # ===== 2. Вид практики =====
        practice_type = extract_practice_type(practice_text)

        # ===== 3. Дата собрания =====
        meeting_date = extract_meeting_date(raw_dates)

        result.append(
            [
                i + 1,  # №
                group,
                direction,
                semester or "",
                practice_type,
                meeting_date,
            ]
        )

    return result


# --- Вспомогательные функции:


def extract_practice_type(text):
    # Оставляем только "Учебная практика ..." или "Производственная практика ..."
    match = re.search(r"(Учебная практика|Производственная практика)[^\n]*", text, re.IGNORECASE)
    return match.group(0).strip().capitalize() if match else ""


def extract_first_month(text):
    # Ищем первую дату в формате дд.мм или дд.мм.гггг
    match = re.search(r"\b(\d{1,2})[./](\d{1,2})([./](\d{4}))?", text)
    if match:
        month = int(match.group(2))
        return month
    return None


def extract_meeting_date(text):

    text = text.replace("\n", " ").replace("г.", "").replace("г", "").strip()

    # Ищем все даты (одна или две)
    date_matches = re.findall(r"(\d{1,2})[./-](\d{1,2})(?:[./-](\d{4}))?", text)

    if not date_matches:
        return ""

    day, month, *year1 = date_matches[0]
    day = int(day)
    month = int(month)

    # Подбор года
    year = None
    if year1 and year1[0]:
        year = int(year1[0])
    elif len(date_matches) > 1:
        # Попробуем взять год из второй даты
        second = date_matches[1]
        if len(second) == 3 and second[2].isdigit():
            year = int(second[2])

    if not year:
        year = datetime.now().year  # fallback, если ничего нет

    try:
        date_obj = datetime(day=day, month=month, year=year)
        return date_obj.strftime("%d.%m.%Y")
    except ValueError:
        return ""


# Функция для чтения плана
def read_plan_from_docx(docx_path):
    """
    Читает первую таблицу из Word-документа и возвращает список списков.
    - Первая строка используется как заголовки.
    - Вторая строка (обычно объединённая и пустая) пропускается.
    - Остальные строки — данные (начиная с третьей строки).
    """
    doc = Document(docx_path)
    table = doc.tables[0]

    data = []

    # Получаем заголовки из первой строки
    headers = [cell.text.strip() for cell in table.rows[0].cells]
    data.append(headers)

    # Пропускаем вторую строку (индекс 1), читаем с третьей
    for row in table.rows[2:]:
        row_data = [cell.text.strip() for cell in row.cells]
        # Добавляем только если в строке есть хотя бы одно непустое значение
        if any(row_data):
            data.append(row_data)

    return data


def find_column_index_by_keyword(model, keyword: str) -> int:
    """Ищет столбец, в заголовке которого содержится keyword (без учёта регистра)."""
    keyword = keyword.lower()
    for col in range(model.columnCount()):
        header = model.headerData(col, Qt.Horizontal, Qt.DisplayRole)
        if header and keyword in str(header).lower():
            return col
    return -1


def clean_practice_name(text):
    """
    Удаляет из строки слова "курс", "семестр" и все цифры.

    Args:
        text (str): Исходная строка.

    Returns:
        str: Очищенная строка.
    """
    # Удаляем слова "курс" и "семестр" (регистронезависимо)
    text = re.sub(r"\b(курс|семестр)\b", "", text, flags=re.IGNORECASE)

    # Удаляем все цифры
    text = re.sub(r"\d+", "", text)

    text = text.replace(":", "")

    # Удаляем лишние пробелы и возвращаем результат
    return " ".join(text.split()).strip()


# функция для обработки данных, загруженных из Excel таблицы
def transform_practice_data(data, start_id=0):
    """
    Преобразует иерархические данные о практиках в плоский список списков.

    Args:
        data: Исходные данные (список словарей с ключами 'title' и 'data')
        start_id: Начальное значение ID (по умолчанию 0)

    Returns:
        Список списков с заданной структурой:
        [id, № группы, сроки, "Кафедра", "", ФИО, "", направление, "нет", "", название практики]
    """
    result = []
    current_id = start_id

    for practice in data:
        title = practice["title"]
        # Пропускаем строку заголовков (первую строку в data)
        for row in practice["data"][1:]:
            if len(row) >= 5:  # Проверяем, что в строке достаточно данных
                transformed_row = [
                    current_id,  # Уникальный ID
                    row[1],  # № группы
                    clean_practice_name(title),  # Название практики из title
                    row[4],  # Сроки прохождения
                    "Кафедра",  # Кафедра (везде одинаково)
                    "",  # Пустая строка
                    row[2].strip(),  # ФИО преподавателя (убираем лишние пробелы)
                    "",  # Пустая строка
                    row[3],  # Направление
                    "нет",  # "нет" (везде одинаково)
                    "",  # Пустая строка
                ]
                result.append(transformed_row)
                current_id += 1

    return result


# Функция для вычленения блоков из таблицы с практиками
def extract_practice_blocks_with_empty_stop(df):
    practice_blocks = []
    current_block = None
    cols_to_extract = 5  # Количество столбцов для вывода
    inside_block = False  # Флаг нахождения внутри блока данных

    for index, row in df.iterrows():
        # Проверяем первую ячейку строки на пустоту
        first_cell_empty = pd.isna(row[0]) or str(row[0]).strip() == ""

        # Если встретили заголовок практики
        if not first_cell_empty and any(
            phrase in str(row[0]).lower()
            for phrase in ["учебная практика", "производственная практика"]
        ):
            # Сохраняем предыдущий блок (если есть)
            if current_block:
                practice_blocks.append(current_block)

            # Начинаем новый блок
            current_block = {"title": str(row[0]), "data": []}
            inside_block = True  # Входим в режим сбора данных
            continue

        # Если внутри блока данных и встретили пустую ячейку в первом столбце
        if inside_block and first_cell_empty:
            inside_block = False  # Прекращаем сбор
            continue

        # Если находимся внутри блока и строка не пустая
        if inside_block and current_block:
            # Берем данные из первых 5 столбцов
            row_data = list(row[:cols_to_extract].values)
            # Проверяем, что в строке есть данные (хотя бы одна непустая ячейка)
            if any(pd.notna(x) and str(x).strip() != "" for x in row_data):
                current_block["data"].append(row_data)

    # Добавляем последний блок, если он не был добавлен
    if current_block:
        practice_blocks.append(current_block)

    return practice_blocks


# Тут порпобую грузить нагрузку
def format_teacher_name(name: str) -> str:
    """Форматирует ФИО преподавателя — делает заглавными только первые буквы."""
    parts = name.strip().split()
    return " ".join(p.capitalize() for p in parts)


def normalize_practice_type(practice: str) -> str:
    """Преобразует названия практик согласно правилам."""
    practice = practice.strip().lower()

    if "ознакомительная" in practice:
        return "Учебная практика – ознакомительная"
    elif "технологическая" in practice or "проектно-технологическая" in practice:
        return "Учебная практика – технологическая (проектно-технологическая)"
    elif "эксплуатационная" in practice:
        return "Производственная практика – эксплуатационная"
    elif "научно-исследовательская работа" in practice and "практика по получению" not in practice:
        return "Производственная практика: Научно-исследовательская работа"
    elif "по получению навыков научно-исследовательской работы" in practice:
        return "Производственная практика по получению навыков научно-исследовательской работы"
    return practice  # если не найдено соответствие — оставить как есть


def extract_additional_info_form_nagruzka(df):
    result_dict = {}
    for idx, row in df.iterrows():
        if idx == 0:
            continue
        group = row[4]

        if pd.isna(group):
            continue
        budget = int(row[5]) if not pd.isna(row[5]) else 0
        paid = int(row[6]) if not pd.isna(row[6]) else 0
        total = int(row[7]) if not pd.isna(row[7]) else budget + paid
        targeted = total - budget - paid if total > budget + paid else 0
        student_info = f"\nГ/б - {budget}\nПл. - {paid}\nЦелевики - {targeted}"
        if group not in result_dict:
            result_dict[group] = student_info
        else:
            continue
    return result_dict


def extract_data(df):
    results = []
    bachelor_list = []
    master_list = []
    for idx, row in df.iterrows():
        if idx == 0:
            continue
        group = row[4]
        if pd.isna(group):
            continue

        num = len(bachelor_list) + len(master_list) + 1
        practice_raw = str(row[12]) if not pd.isna(row[12]) else ""
        practice_type = normalize_practice_type(practice_raw)

        budget = int(row[5]) if not pd.isna(row[5]) else 0
        paid = int(row[6]) if not pd.isna(row[6]) else 0
        total = int(row[7]) if not pd.isna(row[7]) else budget + paid
        targeted = total - budget - paid if total > budget + paid else 0
        student_info = f"Г/б - {budget}\nПл. - {paid}\nЦелевики - {targeted}"
        practice_full = f"{practice_type}\n{student_info}"

        teacher_raw = str(row[16]) if not pd.isna(row[16]) else ""
        teacher_match = re.match(
            r"^([А-ЯЁа-яёA-Za-z\-]+(?:\s+[А-ЯЁа-яёA-Za-z]\.){1,2})", teacher_raw.strip()
        )
        teacher = format_teacher_name(teacher_match.group(1)) if teacher_match else ""

        specialty_raw = str(row[8]) if not pd.isna(row[8]) else ""
        specialty = specialty_raw.split()[0] if specialty_raw else ""

        note = row[29] if not pd.isna(row[29]) else ""

        sroki = str(row[13]) if not pd.isna(row[13]) else ""

        # Сроки пока оставим пустыми (нужен анализ), заполним позже
        edu_lvl = str(row[10]).strip().lower()

        result_row = [
            num,
            group,
            practice_full,
            sroki,
            "Кафедра",
            "",
            teacher,
            "",
            specialty,
            "нет",
            note,
        ]
        if "маг" in edu_lvl:
            master_list.append(result_row)
        else:
            bachelor_list.append(result_row)

    bachelor_list.sort(key=lambda x: x[1])
    master_list.sort(key=lambda x: x[1])
    results = bachelor_list + master_list

    for i in range(len(results)):
        results[i][0] = i + 1
    return results


# Блок для оформления Word документа
# Функция для установки границ у ячейки
def set_cell_border(cell, **kwargs):
    """
    Устанавливает границы ячейки.
    Параметры можно передавать как: top="single", bottom="single", left="single", right="single"
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = f"w:{edge}"
            element = OxmlElement(tag)
            element.set(qn("w:val"), edge_data)  # тип линии
            element.set(qn("w:sz"), "4")  # толщина (1/8 pt)
            element.set(qn("w:space"), "0")  # отступ
            element.set(qn("w:color"), "000000")  # цвет (чёрный)
            tcBorders.append(element)
    tcPr.append(tcBorders)

    # Установка шрифта Times New Roman, размер 10 pt


def set_cell_font(cell, font_name="Times New Roman", font_size=10):
    paragraph = cell.paragraphs[0]
    run = paragraph.runs[0] if paragraph.runs else paragraph.add_run()
    font = run.font
    font.name = font_name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), font_name)
    font.size = Pt(font_size)

    # Заполнение строки word


def fill_the_table_rows(table, data, start_row):
    for i, row_data in enumerate(data):
        # Если строки не хватает — добавляем
        row_index = start_row + i
        if start_row + i >= len(table.rows):
            table.add_row()

        for j, value in enumerate(row_data):
            cell = table.cell(row_index, j)
            cell.text = str(value)
            set_cell_font(cell, font_name="Times New Roman", font_size=10)
            set_cell_border(cell, top="single", bottom="single", left="single", right="single")


# Заполнение столбца word
def fill_the_table_col(table, column_index, data):
    for i, group in enumerate(data):
        row_index = i + 2  # начинаем с 3-й строки
        if row_index >= len(table.rows):
            table.add_row()
        cell = table.rows[row_index].cells[column_index]
        cell.text = group
        set_cell_font(cell, font_name="Times New Roman", font_size=10)
        set_cell_border(cell, top="single", bottom="single", left="single", right="single")
