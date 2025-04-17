import pandas as pd


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

                # Если внутри ббора данных и встретили пустую ячейку в первом столбце
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