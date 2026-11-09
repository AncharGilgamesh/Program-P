"""Here are the models"""

from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex


class PlanTableModel(QAbstractTableModel):
    def __init__(self, data=[], header=None, editable=True):
        super(PlanTableModel, self).__init__()
        self._data = data if data else []
        self._header = header if header else []
        self._editable = editable

    def setData(self, index, value, role=Qt.EditRole):
        if not self._editable or not index.isValid() or role != Qt.EditRole:
            return False

        row, col = index.row(), index.column()

        # Изменяем данные во внутренней структуре
        self._data[row][col] = value

        # Уведомляем View об изменении (ВАЖНО!)
        self.dataChanged.emit(index, index, [role])

        return True

    def flags(self, index):
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if self._editable:
            flags |= Qt.ItemIsEditable
        return flags

    def rowCount(self, index=None):
        """func."""
        if self._data:
            return len(self._data)
        return 0

    def columnCount(self, index=None):
        """func."""
        if self._data:
            return len(self._data[0])
        return len(self._header)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """func."""
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section < len(self._header):
                    return self._header[section]
                else:
                    return "Проверка"

    def insertRows(self, position, rows, values=None, parent=QModelIndex()):
        """Ваша функция с небольшими изменениями"""
        self.beginInsertRows(parent, position, position + rows - 1)
        if values is None:
            values = [["" for _ in range(self.columnCount())] for _ in range(rows)]
        self._data[position:position] = values  # Вставляем в нужную позицию
        self.endInsertRows()
        return True

    def clear(self):
        """Сбрасывает строки через reset, не подменяя _data снаружи модели."""
        self.beginResetModel()
        self._data = []
        self.endResetModel()

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and index.isValid():
            return self._data[index.row()][index.column()]
        if role == Qt.EditRole:
            row = index.row()
            column = index.column()
            return self._data[row][column]
        return None

    def get_column_values(self, column_index):
        """Возвращает список значений из указанного столбца."""
        if not 0 <= column_index < self.columnCount():
            return []  # Проверка на выход за границы

        return [str(row[column_index]) for row in self._data]

    def get_data(self):
        """func."""
        return self._data

    def get_row(self, row):
        return self._data[row]

    def get_col(self, col_index):
        """Возвращает список значений из указанного столбца."""
        if not (0 <= col_index < self.columnCount()):
            return []
        return [self._data[row][col_index] for row in range(self.rowCount())]

    def set_col(self, col_index, values):
        """Устанавливает переданные значения в указанный столбец (values — список)."""
        if not (0 <= col_index < self.columnCount()):
            return

        row_count = self.rowCount()
        for row in range(min(row_count, len(values))):
            self._data[row][col_index] = values[row]

        # Уведомляем представление о массовом изменении данных
        top_left = self.index(0, col_index)
        bottom_right = self.index(self.rowCount() - 1, col_index)
        self.dataChanged.emit(top_left, bottom_right, [Qt.DisplayRole])

    def get_data_without_id(self):
        """Возвращает данные без первого столбца (id)."""
        return [row[1:] for row in self._data]

    def get_header(self):
        """Get header."""
        return self._header

    def add_info_to_cell_by_condition(self, check_col, condition, target_col, new_value):
        """Добавляет new_value в target_col, если check_col удовлетворяет condition."""
        changed_indexes = []  # Запоминаем изменённые ячейки для обновления View

        for row in range(self.rowCount()):
            check_val = self._data[row][check_col]

            # Проверяем условие
            if callable(condition):
                condition_met = condition(check_val)  # Если condition — функция
            else:
                condition_met = check_val == condition  # Если condition — значение

            if not condition_met:
                continue  # Условие не выполнено — пропускаем строку

            # Получаем текущее значение в target_col (если None, заменяем на 0 или "")
            current_val = self._data[row][target_col]
            if current_val is None:
                current_val = 0 if isinstance(new_value, (int, float)) else ""

            # Вычисляем новое значение
            if callable(new_value):
                add_val = new_value(check_val)  # Если new_value — функция
            else:
                add_val = new_value  # Если new_value — число/строка

            # Записываем новое значение (сложение чисел или конкатенация строк)
            self._data[row][target_col] = current_val + add_val
            changed_indexes.append(self.index(row, target_col))  # Запоминаем изменённую ячейку

        # Обновляем только изменённые ячейки в TableView
        if changed_indexes:
            self.dataChanged.emit(changed_indexes[0], changed_indexes[-1], [Qt.DisplayRole])

    def updateCellsByCondition(self, check_col, condition, target_col, new_value):
        for row in range(len(self._data)):
            check_val = self._data[row][check_col]

            if callable(condition):
                meets_cond = condition(check_val)
            else:
                meets_cond = check_val == condition

            if meets_cond:
                if callable(new_value):
                    self._data[row][target_col] = new_value(check_val)
                else:
                    self._data[row][target_col] = new_value

        # Уведомляем view об изменениях
        top_left = self.index(0, 0)
        bottom_right = self.index(self.rowCount() - 1, self.columnCount() - 1)
        self.dataChanged.emit(top_left, bottom_right, [Qt.DisplayRole])

    def fill_column_with_value(self, column_index, value):
        """Заполняет весь столбец заданным значением."""
        if not 0 <= column_index < self.columnCount():
            return  # Защита от выхода за границы

        for row in range(self.rowCount()):
            self._data[row][column_index] = value

        # Уведомляем view об изменениях в столбце
        top_left = self.index(0, column_index)
        bottom_right = self.index(self.rowCount() - 1, column_index)
        self.dataChanged.emit(top_left, bottom_right, [Qt.DisplayRole])


class ResultTableModel(PlanTableModel):
    def __init__(self, data, headers):
        super().__init__(data, headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row, col = index.row(), index.column()

        if role == Qt.DisplayRole:
            if col == 6:  # "Не защитило"
                try:
                    total = int(self._data[row][1])
                    scores = [int(self._data[row][i] or 0) for i in range(2, 6)]
                    return str(max(total - sum(scores), 0))
                except (TypeError, ValueError):
                    return "-"
            value = self._data[row][col]
            return str(value) if value not in [None, "", "0"] else "-"

        return super().data(index, role)

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() or role != Qt.EditRole:
            return False

        row, col = index.row(), index.column()

        if col == 6:
            return False  # "Не защитило" вычисляется

        try:
            if col in [1, 2, 3, 4, 5]:
                value_int = int(value)
                if value_int < 0:
                    return False  # не разрешаем отрицательные значения
            else:
                value_int = value  # строка (например, "Место")
        except ValueError:
            return False  # не число — не сохраняем

        # Предварительно проверим сумму оценок
        if col in [2, 3, 4, 5]:
            try:
                new_score = int(value)
                scores = [int(self._data[row][i] or 0) for i in [2, 3, 4, 5]]
                scores[col - 2] = new_score  # заменим редактируемый
                total = int(self._data[row][1])
                if sum(scores) > total:
                    return False
            except (TypeError, ValueError):
                return False

        if col == 1:  # при изменении "Всего" тоже проверим
            try:
                total = int(value)
                scores = [int(self._data[row][i] or 0) for i in [2, 3, 4, 5]]
                if sum(scores) > total:
                    return False
            except (TypeError, ValueError):
                return False

        self._data[row][col] = str(value).strip()
        self.dataChanged.emit(index, index)

        # Обновим ячейку "Не защитило"
        if col in [1, 2, 3, 4, 5]:
            self.dataChanged.emit(self.index(row, 6), self.index(row, 6))

        return True

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        col = index.column()
        if col == 0 or col == 6:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable  # Только чтение

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def get_data(self):
        result = []
        for row in range(self.rowCount()):
            row_data = []
            for col in range(self.columnCount()):
                index = self.index(row, col)
                value = self.data(index, Qt.DisplayRole)
                if value == "-":
                    value = ""
                row_data.append(value)
            result.append(row_data)
        return result
