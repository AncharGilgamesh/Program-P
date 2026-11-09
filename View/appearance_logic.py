import os
import sqlite3

from PySide6.QtWidgets import QDialog, QMessageBox
from View.appearance import Ui_Dialog

import Models.dbhandler_new as dbh

AUTH_FAILED = "Неверный логин или пароль"
REGISTRATION_CODE_ENV = "REGISTRATION_CODE"


def load_local_env():
    """Подхватывает .env из корня проекта, не затирая уже заданные переменные."""
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    if not os.path.isfile(env_path):
        return
    with open(env_path, encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def registration_failure(code):
    """None, если код принят. Иначе текст отказа, без сравнения с литералом в коде."""
    load_local_env()
    expected = os.environ.get(REGISTRATION_CODE_ENV, "").strip()
    if not expected:
        return "Регистрация недоступна: не задан код регистрации"
    if code != expected:
        return "Неправильный код регистрации"
    return None


class AppearanceDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.success = False
        self.user = None
        self.go_to_auth()

        self.ui.authPagePushButton.clicked.connect(self.go_to_auth)
        self.ui.regPagePushButton.clicked.connect(self.go_to_register)
        self.ui.recoverPagePushButton.clicked.connect(self.go_to_recover)

        self.ui.authPushButton.clicked.connect(self.check_login)
        self.ui.registerButton.clicked.connect(self.register_user)
        self.ui.recoverPushButton.clicked.connect(self.check_recover)

    def go_to_auth(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)
        self.ui.mainInfoLabel.setText("Авторизация")

    def go_to_register(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
        self.ui.mainInfoLabel.setText("Регистрация")

    def go_to_recover(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_3)
        self.ui.mainInfoLabel.setText("Восстановление")

    def check_login(self):
        username = self.ui.authUsernameLine.text()
        password = self.ui.authPassLine.text()
        try:
            accepted = dbh.authenticate(username, password)
        except sqlite3.Error as exc:
            QMessageBox.warning(self, "Ошибка", f"Не удалось проверить учётную запись: {exc}")
            return
        if not accepted:
            QMessageBox.warning(self, "Ошибка", AUTH_FAILED)
            return
        if self.ui.checkBox.isChecked():
            dbh.update_remember_status(username, 1)
        self.success = True
        self.user = username
        self.accept()

    def register_user(self):
        username = self.ui.regUsernamLine.text()
        password = self.ui.regPassLine.text()
        password_rep = self.ui.regRepeatPassLine.text()
        name = self.ui.nameLine.text()
        sec_name = self.ui.familiaLine.text()
        middle_name = self.ui.otchestvoLine.text()
        reg_code = self.ui.regCodeLine.text()
        failure = registration_failure(reg_code)
        if failure:
            QMessageBox.warning(self, "Ошибка", failure)
            return
        if not password == password_rep:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
            return
        if not all([username, password, name, sec_name, middle_name, reg_code]):
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните обязательные поля.")
            return
        try:
            teachers = dbh.select_teacher_by_name(sec_name, name, middle_name)
        except sqlite3.Error as exc:
            QMessageBox.warning(self, "Ошибка", f"Не удалось проверить преподавателя: {exc}")
            return
        if not teachers:
            QMessageBox.warning(self, "Ошибка", "Преподаватель не найден в справочнике")
            return
        try:
            dbh.insert_user(
                teachers[0][0], username, password, sec_name, name, middle_name
            )
        except sqlite3.Error as exc:
            QMessageBox.warning(
                self,
                "Ошибка",
                f"Не удалось зарегистрировать пользователя. Попробуйте другое имя: {exc}",
            )
            return
        QMessageBox.information(self, "Успешно", "Пользователь зарегистрирован")

    def check_recover(self):
        username = self.ui.recoverUsernameLine.text()
        recoverCode = self.ui.revocerRegisterCodeLine.text()
        password = self.ui.recoverPassLine.text()
        repeat_password = self.ui.recoverRepeatPassLine.text()
        failure = registration_failure(recoverCode)
        if failure:
            QMessageBox.warning(self, "Ошибка", failure)
            return
        try:
            users = dbh.select_user_by_username(username)
        except sqlite3.Error as exc:
            QMessageBox.warning(self, "Ошибка", f"Не удалось проверить учётную запись: {exc}")
            return
        if not users:
            QMessageBox.warning(self, "Ошибка", AUTH_FAILED)
            return
        if not password == repeat_password:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
            return
        try:
            dbh.update_user_password(username, password)
        except sqlite3.Error as exc:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сменить пароль: {exc}")
            return
        QMessageBox.information(self, "Успешно", "Успешная смена пароля")

    def get_username(self):
        return self.user

    def get_success_status(self):
        return self.success
