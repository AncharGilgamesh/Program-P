from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QListView, QPushButton, QTextEdit,
    QLineEdit, QLabel, QWidget, QMessageBox, QComboBox
)
from PySide6.QtCore import QStringListModel, Qt
from Models.datahandler import resource_path


class GroupEditDialog(QDialog):
    def __init__(self, all_groups, field_label="Значение", title="Редактирование", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(600, 400)

        with open(resource_path("View/dialogstyle.qss"), "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        # Полные списки
        self._full_all_list = sorted(all_groups)
        self._full_selected_list = []

        # Модели
        self.all_model = QStringListModel(self._full_all_list)
        self.selected_model = QStringListModel([])

        # Элементы управления
        self.search_filter_combo = QComboBox()
        self.search_filter_combo.addItems([
            "Искать везде",
            "Только в доступных группах",
            "Только в выбранных группах"
        ])

        self.search_line = QLineEdit()
        self.search_line.setPlaceholderText("Поиск группы...")

        self.all_list = QListView()
        self.all_list.setModel(self.all_model)

        self.selected_list = QListView()
        self.selected_list.setModel(self.selected_model)

        self.all_list.doubleClicked.connect(self.move_to_selected)
        self.selected_list.doubleClicked.connect(self.move_to_all)

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
        layout.addWidget(self.search_filter_combo)
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

        # Сигналы поиска
        self.search_line.textChanged.connect(self.filter_groups)
        self.search_filter_combo.currentIndexChanged.connect(
            lambda: self.filter_groups(self.search_line.text())
        )

    def filter_groups(self, text):
        mode = self.search_filter_combo.currentIndex()

        if mode in (0, 1):  # Искать везде или в доступных
            filtered_all = [g for g in self._full_all_list if text.lower() in g.lower()]
            self.all_model.setStringList(filtered_all)
        else:
            self.all_model.setStringList(self._full_all_list)

        if mode in (0, 2):  # Искать везде или в выбранных
            filtered_selected = [g for g in self._full_selected_list if text.lower() in g.lower()]
            self.selected_model.setStringList(filtered_selected)
        else:
            self.selected_model.setStringList(self._full_selected_list)

    def move_to_selected(self, index=None):
        if index:
            selected = [self.all_model.data(index, Qt.DisplayRole)]
        else:
            selected = [self.all_model.data(i, Qt.DisplayRole) for i in self.all_list.selectedIndexes()]
        if not selected:
            return
        self._full_selected_list = sorted(set(self._full_selected_list).union(selected))
        self._full_all_list = [g for g in self._full_all_list if g not in selected]
        self.filter_groups(self.search_line.text())

    def move_to_all(self, index=None):
        if index:
            selected = [self.selected_model.data(index, Qt.DisplayRole)]
        else:
            selected = [self.selected_model.data(i, Qt.DisplayRole) for i in self.selected_list.selectedIndexes()]
        if not selected:
            return
        self._full_all_list = sorted(set(self._full_all_list).union(selected))
        self._full_selected_list = [g for g in self._full_selected_list if g not in selected]
        self.filter_groups(self.search_line.text())


    def get_result(self):
        return self._full_selected_list, self.input_edit.toPlainText()
