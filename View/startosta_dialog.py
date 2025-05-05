from PySide6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QComboBox, QPushButton, QFormLayout, QVBoxLayout, QMessageBox
)

class StarostaDialog(QDialog):
    def __init__(self, teachers, starosta_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Редактировать старосту" if starosta_data else "Добавить старосту")
        self.teachers = teachers  # список кортежей: (id, фамилия, имя, отчество)
        with open("View/dialogstyle.qss", "r") as f:
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
            index = self.teacher_combo.findData(starosta_data.get("teacher_id"))
            if index != -1:
                self.teacher_combo.setCurrentIndex(index)

            self.last_name_edit.setText(starosta_data.get("last_name", ""))
            self.first_name_edit.setText(starosta_data.get("first_name", ""))
            self.middle_name_edit.setText(starosta_data.get("middle_name", ""))
            self.group_edit.setText(starosta_data.get("group_num", ""))
            self.email_edit.setText(starosta_data.get("email", ""))
            self.phone_edit.setText(starosta_data.get("phone", ""))

        # Layout
        form_layout = QFormLayout()
        form_layout.addRow("Куратор:", self.teacher_combo)
        form_layout.addRow("Фамилия:", self.last_name_edit)
        form_layout.addRow("Имя:", self.first_name_edit)
        form_layout.addRow("Отчество:", self.middle_name_edit)
        form_layout.addRow("Группа:", self.group_edit)
        form_layout.addRow("Почта:", self.email_edit)
        form_layout.addRow("Номер:", self.phone_edit)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.save_btn)
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
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните обязательные поля.")
            return

        self.result = [
            teacher_id,
            last_name,
            first_name,
            middle_name,
            group,
            email,
            phone
        ]
        self.accept()
