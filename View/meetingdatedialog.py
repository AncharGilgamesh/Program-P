from PySide6.QtWidgets import (
    QDialog,
    QListView,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QDateEdit,
    QAbstractItemView,
)
from PySide6.QtCore import QStringListModel, QDate


class MeetingDateDialog(QDialog):
    def __init__(self, group_practice_list, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Назначить дату собрания")
        self.resize(600, 400)

        # Модели
        self.left_model = QStringListModel(group_practice_list)
        self.right_model = QStringListModel([])

        # Виджеты списков
        self.left_view = QListView()
        self.left_view.setModel(self.left_model)
        self.left_view.setSelectionMode(QAbstractItemView.MultiSelection)

        self.right_view = QListView()
        self.right_view.setModel(self.right_model)
        self.right_view.setSelectionMode(QAbstractItemView.MultiSelection)

        # Кнопки перемещения
        self.btn_add = QPushButton("→")
        self.btn_remove = QPushButton("←")

        # Дата
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())

        # Кнопки действия
        self.ok_btn = QPushButton("Применить")
        self.cancel_btn = QPushButton("Отмена")

        # Слои
        move_layout = QVBoxLayout()
        move_layout.addWidget(self.btn_add)
        move_layout.addWidget(self.btn_remove)

        list_layout = QHBoxLayout()
        list_layout.addWidget(self.left_view)
        list_layout.addLayout(move_layout)
        list_layout.addWidget(self.right_view)

        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Дата собрания:"))
        date_layout.addWidget(self.date_edit)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.ok_btn)
        buttons_layout.addWidget(self.cancel_btn)

        layout = QVBoxLayout()
        layout.addLayout(list_layout)
        layout.addLayout(date_layout)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)

        # Сигналы
        self.btn_add.clicked.connect(self.move_to_right)
        self.btn_remove.clicked.connect(self.move_to_left)
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

    def move_to_right(self):
        selected = self.left_view.selectionModel().selectedIndexes()
        items = self.left_model.stringList()
        right = self.right_model.stringList()

        for i in sorted(selected, reverse=True):
            right.append(items[i.row()])
            items.pop(i.row())

        self.left_model.setStringList(items)
        self.right_model.setStringList(right)

    def move_to_left(self):
        selected = self.right_view.selectionModel().selectedIndexes()
        items = self.right_model.stringList()
        left = self.left_model.stringList()

        for i in sorted(selected, reverse=True):
            left.append(items[i.row()])
            items.pop(i.row())

        self.left_model.setStringList(left)
        self.right_model.setStringList(items)

    def get_results(self):
        selected = self.right_model.stringList()
        date_str = self.date_edit.date().toString("dd.MM.yyyy")
        return selected, date_str
