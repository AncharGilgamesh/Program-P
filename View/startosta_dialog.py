from PySide6.QtWidgets import (
    QDialog,
    QLineEdit,
    QComboBox,
    QPushButton,
    QFormLayout,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox,
)
from Models.datahandler import resource_path


class StarostaDialog(QDialog):
    def __init__(self, teachers, starosta_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Изменить старосту" if starosta_data else "Добавить старосту")
        self.setMinimumWidth(440)
        self.teachers = teachers  # список кортежей: (id, фамилия, имя, отчество)

        with open(resource_path("View/dialogstyle.qss"), "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        # Элементы интерфейса
        self.teacher_combo = QComboBox()
        self.last_name_edit = QLineEdit()
        self.first_name_edit = QLineEdit()
        self.middle_name_edit = QLineEdit()
        self.group_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.phone_edit = QLineEdit()
        self.save_btn = QPushButton("Сохранить")

        # Заполнение комбобокса
        for teacher in self.teachers:
            teacher_id = teacher[0]
            fio = f"{teacher[1]} {teacher[2]} {teacher[3]}"
            self.teacher_combo.addItem(fio, teacher_id)

        # Заполнение при редактировании
        if starosta_data:
            index = self.teacher_combo.findData(starosta_data[0])  # teacher_id
            if index != -1:
                self.teacher_combo.setCurrentIndex(index)

            self.last_name_edit.setText(starosta_data[1] or "")
            self.first_name_edit.setText(starosta_data[2] or "")
            self.middle_name_edit.setText(starosta_data[3] or "")
            self.group_edit.setText("" if starosta_data[4] is None else str(starosta_data[4]))
            self.email_edit.setText(starosta_data[5] or "")
            self.phone_edit.setText(starosta_data[6] or "")

        # Layout
        form_layout = QFormLayout()
        form_layout.addRow("Куратор:", self.teacher_combo)
        form_layout.addRow("Фамилия:", self.last_name_edit)
        form_layout.addRow("Имя:", self.first_name_edit)
        form_layout.addRow("Отчество:", self.middle_name_edit)
        form_layout.addRow("Группа:", self.group_edit)
        form_layout.addRow("Почта:", self.email_edit)
        form_layout.addRow("Телефон:", self.phone_edit)

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)
        buttons = QHBoxLayout()
        buttons.addWidget(self.save_btn)
        buttons.addWidget(self.cancel_btn)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addLayout(buttons)
        self.setLayout(layout)

        self.result = None
        self.save_btn.clicked.connect(self.on_save)

    def get_data(self):
        return self.result

    def on_save(self):
        teacher_id = self.teacher_combo.currentData()
        last_name = self.last_name_edit.text().strip()
        first_name = self.first_name_edit.text().strip()
        middle_name = self.middle_name_edit.text().strip()
        group = self.group_edit.text().strip()
        email = self.email_edit.text().strip()
        phone = self.phone_edit.text().strip()

        if not all([teacher_id, last_name, first_name, group, email]):
            QMessageBox.warning(
                self, "Ошибка", "Заполните куратора, фамилию, имя, группу и почту."
            )
            return

        self.result = [teacher_id, last_name, first_name, middle_name, group, email, phone]
        self.accept()
