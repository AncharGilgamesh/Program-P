from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QPushButton,
    QHBoxLayout,
)
from Models.datahandler import resource_path


DEGREE_ITEMS = ["", "к.т.н.", "к.ф.-м.н.", "д.ф.-м.н.", "д.т.н.", "-"]
DEGREE_ALIASES = {
    "к.т.н": "к.т.н.",
    "к.ф.м.н": "к.ф.-м.н.",
    "к.ф.-м.н": "к.ф.-м.н.",
    "д.ф.м.н": "д.ф.-м.н.",
    "д.ф.-м.н": "д.ф.-м.н.",
    "д.т.н": "д.т.н.",
    "д.т.н.": "д.т.н.",
}


class PrepodDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Изменить преподавателя" if data else "Добавить преподавателя")
        self.setMinimumWidth(440)
        with open(resource_path("View/dialogstyle.qss"), "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        # Поля
        self.last_name_edit = QLineEdit()
        self.first_name_edit = QLineEdit()
        self.middle_name_edit = QLineEdit()
        self.degree_combo = QComboBox()
        self.degree_combo.addItems(DEGREE_ITEMS)
        self.position_combo = QComboBox()
        self.position_combo.addItems(
            ["", "доцент", "профессор", "ассистент", "Зав. кафедрой", "ст. преподаватель"]
        )
        self.email_edit = QLineEdit()
        self.phone_edit = QLineEdit()

        # Если data передана — заполняем поля
        if data:
            self.last_name_edit.setText(data[0] if len(data) > 0 else "")
            self.first_name_edit.setText(data[1] if len(data) > 1 else "")
            self.middle_name_edit.setText(data[2] if len(data) > 2 else "")
            degree = data[3] if len(data) > 3 else ""
            degree = DEGREE_ALIASES.get(degree, degree)
            if degree and self.degree_combo.findText(degree) < 0:
                self.degree_combo.addItem(degree)
            self.degree_combo.setCurrentText(degree)
            self.position_combo.setCurrentText(data[4] if len(data) > 4 else "")
            self.email_edit.setText(data[5] if len(data) > 5 else "")
            self.phone_edit.setText(data[6] if len(data) > 6 else "")

        # Разметка
        form_layout = QFormLayout()
        form_layout.addRow("Фамилия:", self.last_name_edit)
        form_layout.addRow("Имя:", self.first_name_edit)
        form_layout.addRow("Отчество:", self.middle_name_edit)
        form_layout.addRow("Степень:", self.degree_combo)
        form_layout.addRow("Должность:", self.position_combo)
        form_layout.addRow("Почта:", self.email_edit)
        form_layout.addRow("Телефон:", self.phone_edit)

        # Кнопки
        self.ok_button = QPushButton("Сохранить")
        self.cancel_button = QPushButton("Отмена")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def get_data(self):
        return [
            self.last_name_edit.text(),
            self.first_name_edit.text(),
            self.middle_name_edit.text(),
            self.degree_combo.currentText(),
            self.position_combo.currentText(),
            self.email_edit.text(),
            self.phone_edit.text(),
        ]
