import pandas as pd
import re
from PySide6.QtCore import Qt
from docx.opc.exceptions import PackageNotFoundError
from docx import Document
from datetime import datetime


#Второй этап отчета
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

        result.append([
            number,
            city,
            location,
            people_count,
            placeholder,
            start_date,
            end_date
        ])

    return result


def extract_start_end_dates(text):
    text = text.replace('\n', ' ').replace('г.', '').replace('г', '').strip()
    date_matches = re.findall(r'(\d{1,2})[./-](\d{1,2})(?:[./-](\d{4}))?', text)

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
    except:
        start = ""

    try:
        end = datetime(day=day2, month=month2, year=year2).strftime("%d.%m.%Y") if day2 and month2 else ""
    except:
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
        practice_short = practice.replace(
            "по получению навыков научно-исследовательской работы", "ППНИР"
        ).replace(
            "научно-исследовательская работа", "НИР"
        ).replace(
            "научно-исследовательская  работа", "НИР"
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
        practice_short = practice.replace(
            "по получению навыков научно-исследовательской работы", "ППНИР"
        ).replace(
            "научно-исследовательская работа", "НИР"
        ).replace(
            "научно-исследовательская  работа", "НИР"
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

        result.append([
            i + 1,            # №
            group,
            direction,
            semester or "",
            practice_type,
            meeting_date
        ])

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
        day, month = int(match.group(1)), int(match.group(2))
        return month
    return None

def extract_meeting_date(text):

    text = text.replace('\n', ' ').replace('г.', '').replace('г', '').strip()

    # Ищем все даты (одна или две)
    date_matches = re.findall(r'(\d{1,2})[./-](\d{1,2})(?:[./-](\d{4}))?', text)

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
        title = practice['title']
        # Пропускаем строку заголовков (первую строку в data)
        for row in practice['data'][1:]:
            if len(row) >= 5:  # Проверяем, что в строке достаточно данных
                transformed_row = [
                    current_id,               # Уникальный ID
                    row[1],                  # № группы
                    title,                   # Название практики из title
                    row[4],                  # Сроки прохождения
                    "Кафедра",               # Кафедра (везде одинаково)
                    "",                      # Пустая строка
                    row[2].strip(),          # ФИО преподавателя (убираем лишние пробелы)
                    "",                      # Пустая строка
                    row[3],                  # Направление
                    "нет",                   # "нет" (везде одинаково)
                    ""                       # Пустая строка

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
                first_cell_empty = pd.isna(row[0]) or str(row[0]).strip() == ''

                # Если встретили заголовок практики
                if not first_cell_empty and any(phrase in str(row[0]).lower() 
                                            for phrase in ['учебная практика', 'производственная практика']):
                    # Сохраняем предыдущий блок (если есть)
                    if current_block:
                        practice_blocks.append(current_block)
                    
                    # Начинаем новый блок
                    current_block = {
                        'title': str(row[0]),
                        'data': []
                    }
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
                    if any(pd.notna(x) and str(x).strip() != '' for x in row_data):
                        current_block['data'].append(row_data)

            # Добавляем последний блок, если он не был добавлен
            if current_block:
                practice_blocks.append(current_block)

            return practice_blocks