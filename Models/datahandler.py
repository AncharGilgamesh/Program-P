import pandas as pd
import re
import sys
import os
from PySide6.QtCore import Qt
from docx import Document
from datetime import date, datetime
from collections import defaultdict


# Для превращения относительного пути в абсолютный
def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(project_root, relative_path)


# Шестой этап
def parse_sixth_table(data_rows):
    # те же строки, что у первого этапа, преподаватель в 5 столбце
    result = []
    number = 0
    for row in data_rows:
        if len(row) < 9:
            continue
        number += 1
        teacher = ""
        if len(row) > 5 and row[5] not in (None, ""):
            teacher = str(row[5]).strip()
        group = row[0].strip() if row[0] is not None else ""
        practice = extract_practice_type(str(row[1] or ""))
        result.append([str(number), teacher, "", group, practice, "", "", ""])
    return result


# Пятый этап отчета
def parse_fiveth_table(data):
    # сюда передаю table2, номер группы ищу в тексте места (4xxx)
    result = []
    skipped = 0
    for row in data:
        place = str(row[2]) if len(row) > 2 and row[2] is not None else ""
        match = re.search(r"\b4\d{3}\b", place)
        if not match:
            skipped += 1
            continue
        people_amount = row[3] if len(row) > 3 else ""
        result.append([match.group(), people_amount, "", "", "", "", "", "в КНИТУ-КАИ"])
    return result, skipped


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
        place_with_groups = f"{place}, " + ", ".join(sorted(groups, key=str))
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

        # 4. Сколько человек направлено (Г/б, Пл., Целевики; год в названии не считаю)
        people_count = count_directed_students(practice_text)

        # 5. Пустая строка
        placeholder = ""

        # 6-7. Даты начала и конца практики
        start_date, end_date = extract_start_end_dates(date_text)

        result.append([number, city, location, people_count, placeholder, start_date, end_date])

    return result


def count_directed_students(practice_text):
    total = 0
    for line in str(practice_text).splitlines():
        match = re.search(
            r"(?:Г/б|Пл\.|Целевики)\s*[-–—:]?\s*(\d+)",
            line,
            flags=re.IGNORECASE,
        )
        if match:
            total += int(match.group(1))
    return total


_LEADING_DAY_MONTH = re.compile(r"^\d{1,2}[./]\d{1,2}")
_ISO_DATE = re.compile(r"(\d{4})-(\d{2})-(\d{2})(?:[ T]\d{2}:\d{2}:\d{2})?")


def normalize_practice_period(value):
    # excel и ГГГГ-ММ-ДД -> дд.мм.гггг; то, что уже начинается с дд.мм, не трогаю
    if isinstance(value, datetime):
        return "" if pd.isna(value) else value.strftime("%d.%m.%Y")
    if isinstance(value, date):
        return value.strftime("%d.%m.%Y")
    if value is None or pd.isna(value):
        return ""
    text = str(value).strip()
    if not text or _LEADING_DAY_MONTH.match(text):
        return text
    replaced = 0

    def _as_day_first(match):
        nonlocal replaced
        if replaced >= 2:
            return match.group(0)
        try:
            parsed = datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        except ValueError:
            return match.group(0)
        replaced += 1
        return parsed.strftime("%d.%m.%Y")

    return _ISO_DATE.sub(_as_day_first, text)


def extract_start_end_dates(text):
    text = normalize_practice_period(text)
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
    except (TypeError, ValueError):
        start = ""

    try:
        end = (
            datetime(day=day2, month=month2, year=year2).strftime("%d.%m.%Y")
            if day2 and month2
            else ""
        )
    except (TypeError, ValueError):
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
        # Вторая цифра номера группы — курс. Осень (месяцы 7–12) — нечётный семестр,
        # весна (1–6) — чётный. Группа *4** в сентябре даёт 7, в феврале — 8.
        semester = None
        if course_digit:
            if month and 1 <= month <= 6:
                semester = course_digit * 2
            elif month and 6 < month <= 12:
                semester = course_digit * 2 - 1

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
    source = "" if text is None else str(text)
    match = re.search(
        r"(Учебная практика|Производственная практика)[^\n]*", source, re.IGNORECASE
    )
    if match:
        return match.group(0).strip().capitalize()
    without = _STUDENT_BLOCK_AT_END.sub("", source)
    for line in without.splitlines():
        if line.strip():
            return line.strip()
    return ""


def extract_first_month(text):
    # Ищем первую дату в формате дд.мм или дд.мм.гггг
    text = normalize_practice_period(text)
    match = re.search(r"\b(\d{1,2})[./](\d{1,2})([./](\d{4}))?", text)
    if match:
        month = int(match.group(2))
        return month
    return None


def extract_meeting_date(text):

    text = normalize_practice_period(text)
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


def rows_from_saved_report(doc, start_rows, widths):
    if len(doc.tables) < 6:
        raise ValueError("В файле отчёта нужны шесть таблиц")
    loaded = []
    for table, start, width in zip(doc.tables, start_rows, widths):
        rows = []
        for row in table.rows[start:]:
            cells = [cell.text.strip() for cell in row.cells]
            cells = cells[:width]
            if len(cells) < width:
                cells.extend([""] * (width - len(cells)))
            if any(cells):
                rows.append(cells)
        loaded.append(rows)
    return loaded


def rows_from_saved_plan(data):
    rows = []
    for raw in data[1:]:
        cells = ["" if cell is None else str(cell).strip() for cell in raw]
        if not any(cells):
            continue
        cells = cells[:10]
        if len(cells) < 10:
            cells.extend([""] * (10 - len(cells)))
        rows.append(cells)
    return [[index, *cells] for index, cells in enumerate(rows, start=1)]


def find_column_index_by_keyword(model, keyword: str) -> int:
    keyword = keyword.lower()
    for col in range(model.columnCount()):
        header = model.headerData(col, Qt.Horizontal, Qt.DisplayRole)
        if header and keyword in str(header).lower():
            return col
    return -1


def clean_practice_name(text):
    # убираю "курс", "семестр" и цифры
    text = re.sub(r"\b(курс|семестр)\b", "", text, flags=re.IGNORECASE)

    # Удаляем все цифры
    text = re.sub(r"\d+", "", text)

    text = text.replace(":", "")

    # Удаляем лишние пробелы и возвращаем результат
    return " ".join(text.split()).strip()


# функция для обработки данных, загруженных из Excel таблицы
def transform_practice_data(data, start_id=0):
    result = []
    current_id = start_id

    for practice in data:
        title = practice["title"]
        # Пропускаем строку заголовков (первую строку в data)
        for row in practice["data"][1:]:
            if len(row) >= 5:  # Проверяем, что в строке достаточно данных
                group_cell = row[1]
                if group_cell is None or pd.isna(group_cell) or str(group_cell).strip() == "":
                    continue
                direction = row[3]
                if direction is None or pd.isna(direction):
                    direction = ""
                else:
                    direction = str(direction).strip()
                transformed_row = [
                    current_id,  # Уникальный ID
                    normalize_group(group_cell),  # № группы
                    clean_practice_name(title),  # Название практики из title
                    normalize_practice_period(row[4]),  # Сроки прохождения
                    "Кафедра",  # Кафедра (везде одинаково)
                    "",  # Пустая строка
                    "" if pd.isna(row[2]) else str(row[2]).strip(),  # ФИО преподавателя
                    "",  # Пустая строка
                    direction,  # Направление
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
    parts = name.strip().split()
    return " ".join(p.capitalize() for p in parts)


def parse_workload_teacher(value):
    if value is None or pd.isna(value):
        return ""
    text = str(value).strip()
    if not text:
        return ""
    spaced = re.sub(r"\.(\S)", r". \1", text)
    tokens = [token.strip(",;") for token in spaced.split()]
    tokens = [token for token in tokens if token]
    if not tokens or not re.fullmatch(r"[A-Za-zА-ЯЁа-яё\-]{2,}", tokens[0]):
        return ""
    initials = []
    words = []
    for token in tokens[1:]:
        if re.fullmatch(r"[A-Za-zА-ЯЁа-яё]\.", token):
            if words:
                break
            initials.append(token)
        elif re.fullmatch(r"[A-Za-zА-ЯЁа-яё\-]{2,}", token):
            if initials:
                break
            words.append(token)
        else:
            break
    if initials:
        parsed = " ".join([tokens[0], *initials[:2]])
    elif words:
        parsed = " ".join([tokens[0], *words[:2]])
    else:
        return ""
    formatted = format_teacher_name(parsed)
    return re.sub(r"(?<=\.)\s+(?=[A-Za-zА-ЯЁа-яё]\.)", "", formatted)


def normalize_group(value):
    # excel иногда отдаёт 4111.0
    text = str(value).strip()
    if text.endswith(".0") and text[:-2].isdigit():
        return text[:-2]
    return text


def normalize_practice_type(practice: str) -> str:
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


_STUDENT_BLOCK_AT_END = re.compile(r"(?:\n)?Г/б - \d+\nПл\. - \d+\nЦелевики - \d+\s*$")


def apply_student_block(current, block):
    text = "" if current is None else str(current).rstrip()
    addition = str(block).strip()
    without = _STUDENT_BLOCK_AT_END.sub("", text).rstrip()
    if not without:
        return addition
    return f"{without}\n{addition}"


def _cell(row, index):
    try:
        if index >= len(row):
            raise IndexError
        return row[index]
    except (KeyError, IndexError):
        raise IndexError(f"В строке нагрузки нет столбца {index + 1}") from None


def _count_cell(row, index):
    value = _cell(row, index)
    if pd.isna(value):
        return 0
    if isinstance(value, bool):
        raise ValueError(f"Столбец {index + 1} должен быть числом")
    if isinstance(value, str):
        text = value.strip().replace(",", ".")
        if not text:
            return 0
        try:
            number = float(text)
        except ValueError:
            raise ValueError(f"Столбец {index + 1} должен быть числом, получено: {value}") from None
    else:
        try:
            number = float(value)
        except (TypeError, ValueError):
            raise ValueError(f"Столбец {index + 1} должен быть числом, получено: {value}") from None
    if not number.is_integer():
        raise ValueError(f"Столбец {index + 1} должен быть целым числом, получено: {value}")
    return int(number)


def _workload_practice_type(row):
    if len(row) <= 12:
        return ""
    value = row[12]
    if pd.isna(value):
        return ""
    return normalize_practice_type(str(value))


def practice_type_from_plan_cell(value):
    text = "" if value is None else str(value)
    without = _STUDENT_BLOCK_AT_END.sub("", text).strip()
    return normalize_practice_type(without)


def choose_student_block(blocks, group, practice_cell):
    group_key = normalize_group(group)
    exact = blocks.get((group_key, practice_type_from_plan_cell(practice_cell)))
    if exact is not None:
        return exact
    same_group = [
        block
        for key, block in blocks.items()
        if isinstance(key, tuple) and len(key) == 2 and key[0] == group_key
    ]
    if len(same_group) == 1:
        return same_group[0]
    return None


def _student_counts(row):
    budget = _count_cell(row, 5)
    paid = _count_cell(row, 6)
    total_cell = _cell(row, 7)
    if pd.isna(total_cell):
        return budget, paid, 0
    total = _count_cell(row, 7)
    if total < budget + paid:
        group_cell = row[4] if len(row) > 4 else ""
        group = "" if pd.isna(group_cell) else normalize_group(group_cell)
        raise ValueError(
            f"Группа {group}: всего {total} меньше суммы бюджета {budget} и платного {paid}"
        )
    targeted = total - budget - paid if total > budget + paid else 0
    return budget, paid, targeted


def extract_additional_info_form_nagruzka(df):
    totals = {}
    for idx, row in df.iterrows():
        if idx == 0:
            continue
        group = row[4]
        if pd.isna(group):
            continue
        key = (normalize_group(group), _workload_practice_type(row))
        budget, paid, targeted = _student_counts(row)
        previous = totals.get(key, (0, 0, 0))
        totals[key] = (
            previous[0] + budget,
            previous[1] + paid,
            previous[2] + targeted,
        )
    return {
        key: f"\nГ/б - {budget}\nПл. - {paid}\nЦелевики - {targeted}"
        for key, (budget, paid, targeted) in totals.items()
    }


def extract_data(df):
    results = []
    bachelor_list = []
    master_list = []
    for idx, row in df.iterrows():
        if idx == 0:
            continue
        group = row[4]
        if pd.isna(group) or str(group).strip() == "":
            continue
        group = normalize_group(group)

        num = len(bachelor_list) + len(master_list) + 1
        practice_raw = str(row[12]) if not pd.isna(row[12]) else ""
        practice_type = normalize_practice_type(practice_raw)

        budget, paid, targeted = _student_counts(row)
        student_info = f"Г/б - {budget}\nПл. - {paid}\nЦелевики - {targeted}"
        practice_full = f"{practice_type}\n{student_info}"

        teacher = parse_workload_teacher(row[16])

        specialty_raw = str(row[8]) if not pd.isna(row[8]) else ""
        specialty = specialty_raw.split()[0] if specialty_raw else ""

        note_cell = _cell(row, 29)
        note = "" if pd.isna(note_cell) else note_cell

        sroki = normalize_practice_period(row[13])

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
