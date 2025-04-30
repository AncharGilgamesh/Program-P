"""Here are the models"""

from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, QAbstractListModel

class DocTableModel(QAbstractTableModel):
    HEADERS = ["Год", "Тип", "Создано", "Истекает", "Создатель", "Защищено", "Открыть", "Удалить"]

    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self.HEADERS)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        row, col = index.row(), index.column()
        item = self._data[row]

        if role == Qt.DisplayRole:
            if col == 0:
                return item["year"]
            elif col == 1:
                return item["type"]
            elif col == 2:
                return item["created"].toString("dd.MM.yyyy")
            elif col == 3:
                return item["created"].addYears(5).toString("dd.MM.yyyy")
            elif col == 4:
                return item["creator"]
            elif col in [6, 7]:
                return ""  # кнопки

        if role == Qt.CheckStateRole and col == 5:
            return Qt.Checked if item["protected"] else Qt.Unchecked

        return None

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False
        row, col = index.row(), index.column()
        if col == 5 and role == Qt.CheckStateRole:
            self._data[row]["protected"] = (value == Qt.Checked)
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        col = index.column()
        if col == 5:
            return Qt.ItemIsUserCheckable | Qt.ItemIsEnabled
        return Qt.ItemIsEnabled

class PlanTableModel(QAbstractTableModel):
    def __init__(self, data = [], header=None):
        super(PlanTableModel, self).__init__()
        self._data = data if data else []
        self._header = header if header else []
    

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() or role != Qt.EditRole:
            return False
        
        row, col = index.row(), index.column()
        
        # Изменяем данные во внутренней структуре
        self._data[row][col] = value
        
        # Уведомляем View об изменении (ВАЖНО!)
        self.dataChanged.emit(index, index, [role])
        
        return True

    def flags(self, index):
        return (
            Qt.ItemIsEnabled | 
            Qt.ItemIsSelectable | 
            Qt.ItemIsEditable  # Разрешаем редактирование
        )

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
                    return 'Проверка'


    def insertRows(self, position, rows, values=None, parent=QModelIndex()):
        """Ваша функция с небольшими изменениями"""
        self.beginInsertRows(parent, position, position + rows - 1)
        if values is None:
            values = [['' for _ in range(self.columnCount())] for _ in range(rows)]
        self._data[position:position] = values  # Вставляем в нужную позицию
        self.endInsertRows()
        return True

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
    
    def get_data_without_id(self):
        """Возвращает данные без первого столбца (id)."""
        return [row[1:] for row in self._data]

    def get_header(self):
        """Get header."""
        return self._header
    
    def updateCellsByCondition(self, check_col, condition, target_col, new_value):
        for row in range(len(self._data)):
            check_val = self._data[row][check_col]
            
            if callable(condition):
                meets_cond = condition(check_val)
            else:
                meets_cond = (check_val == condition)
            
            if meets_cond:
                if callable(new_value):
                    self._data[row][target_col] = new_value(check_val)
                else:
                    self._data[row][target_col] = new_value
        
        # Уведомляем view об изменениях
        top_left = self.index(0, 0)
        bottom_right = self.index(self.rowCount()-1, self.columnCount()-1)
        self.dataChanged.emit(top_left, bottom_right, [Qt.DisplayRole])

class ResultTableModel(PlanTableModel):
    def __init__(self, data, headers):
        super().__init__(data, headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row, col = index.row(), index.column()

        if role == Qt.DisplayRole:
            if col == 5:  # "Не защитило"
                try:
                    total = int(self._data[row][1])
                    scores = [int(self._data[row][i] or 0) for i in range(2, 5)]
                    return str(max(total - sum(scores), 0))
                except Exception:
                    return "-"
            value = self._data[row][col]
            return str(value) if value not in [None, ""] else "-"

        return super().data(index, role)

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() or role != Qt.EditRole:
            return False

        row, col = index.row(), index.column()

        if col == 5:
            return False  # "Не защитило" вычисляется

        try:
            if col in [1, 2, 3, 4]:
                value_int = int(value)
                if value_int < 0:
                    return False  # не разрешаем отрицательные значения
            else:
                value_int = value  # строка (например, "Место")
        except ValueError:
            return False  # не число — не сохраняем

        # Предварительно проверим сумму оценок
        if col in [2, 3, 4]:
            try:
                new_score = int(value)
                scores = [int(self._data[row][i] or 0) for i in [2, 3, 4]]
                scores[col - 2] = new_score  # заменим редактируемый
                total = int(self._data[row][1])
                if sum(scores) > total:
                    return False
            except:
                return False

        if col == 1:  # при изменении "Всего" тоже проверим
            try:
                total = int(value)
                scores = [int(self._data[row][i] or 0) for i in [2, 3, 4]]
                if sum(scores) > total:
                    return False
            except:
                return False

        self._data[row][col] = str(value).strip()
        self.dataChanged.emit(index, index)

        # Обновим ячейку "Не защитило"
        if col in [1, 2, 3, 4]:
            self.dataChanged.emit(self.index(row, 5), self.index(row, 5))

        return True

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        col = index.column()
        if col == 0 or col == 5:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable  # Только чтение

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
