"""Here are the models"""

from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex, QAbstractListModel

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