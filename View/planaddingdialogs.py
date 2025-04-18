from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QListView, QPushButton, QTextEdit,
    QLineEdit, QLabel, QWidget, QMessageBox
)
from PySide6.QtCore import QStringListModel, Qt
class GroupEditDialog(QDialog):
    def __init__(self, all_groups, field_label="Значение", title="Редактирование", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(600, 400)
        with open("View/dialogstyle.qss", "r") as f:
            self.setStyleSheet(f.read())

        # Модели
        self.all_model = QStringListModel(sorted(all_groups))
        self.selected_model = QStringListModel([])

        # UI
        self.search_line = QLineEdit()
        self.search_line.setPlaceholderText("Поиск группы...")

        self.all_list = QListView()
        self.all_list.setModel(self.all_model)

        self.selected_list = QListView()
        self.selected_list.setModel(self.selected_model)

        self.add_button = QPushButton("→")
        self.remove_button = QPushButton("←")
        self.add_button.clicked.connect(self.move_to_selected)
        self.remove_button.clicked.connect(self.move_to_all)

        self.input_label = QLabel(field_label)
        self.input_edit = QTextEdit()
        self.input_edit.setPlaceholderText(f"Введите {field_label.lower()} для выбранных групп...")

        self.apply_button = QPushButton("Применить")
        self.cancel_button = QPushButton("Отмена")
        self.apply_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.search_line)

        lists_layout = QHBoxLayout()
        lists_layout.addWidget(self.all_list)

        mid_buttons = QVBoxLayout()
        mid_buttons.addStretch()
        mid_buttons.addWidget(self.add_button)
        mid_buttons.addWidget(self.remove_button)
        mid_buttons.addStretch()
        lists_layout.addLayout(mid_buttons)

        lists_layout.addWidget(self.selected_list)
        layout.addLayout(lists_layout)

        layout.addWidget(self.input_label)
        layout.addWidget(self.input_edit)

        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(self.apply_button)
        buttons.addWidget(self.cancel_button)
        layout.addLayout(buttons)

        self.search_line.textChanged.connect(self.filter_groups)

        # Полный список сохраняем отдельно
        self._full_group_list = list(self.all_model.stringList())

    def filter_groups(self, text):
        filtered = [g for g in self._full_group_list if text.lower() in g.lower()]
        self.all_model.setStringList(filtered)

    def move_to_selected(self):
        selected = [self.all_model.data(i, Qt.DisplayRole) for i in self.all_list.selectedIndexes()]
        if not selected:
            return
        current_selected = set(self.selected_model.stringList())
        updated_selected = sorted(current_selected.union(selected))
        self.selected_model.setStringList(updated_selected)
        self._full_group_list = [g for g in self._full_group_list if g not in selected]
        self.all_model.setStringList(self._full_group_list)

    def move_to_all(self):
        selected = [self.selected_model.data(i, Qt.DisplayRole) for i in self.selected_list.selectedIndexes()]
        if not selected:
            return
        current_all = set(self._full_group_list).union(selected)
        self._full_group_list = sorted(current_all)
        self.all_model.setStringList(self._full_group_list)
        remaining = [g for g in self.selected_model.stringList() if g not in selected]
        self.selected_model.setStringList(remaining)

    def get_result(self):
        return self.selected_model.stringList(), self.input_edit.toPlainText()
