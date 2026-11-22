import os
import sqlite3

from PySide6.QtWidgets import QDialog, QMessageBox
from View.appearance import Ui_Dialog

import Models.dbhandler as dbh
from window_support import save_remembered_username

AUTH_FAILED = "Неверный логин или пароль"
EMPTY_NEW_PASSWORD = "Введите новый пароль"
WRONG_CURRENT_PASSWORD = "Неверный текущий пароль"
REGISTRATION_CODE_ENV = "REGISTRATION_CODE"
RESERVED_ADMIN_ENV = "RESERVED_ADMIN"


def reserved_admin_username():
    load_local_env()
    return os.environ.get(RESERVED_ADMIN_ENV, "").strip()


def is_reserved_admin(username):
    expected = reserved_admin_username()
    if not expected:
        return False
    return str(username or "").strip().lower() == expected.lower()


def canonical_username(username):
    text = str(username or "").strip()
    if is_reserved_admin(text):
        return reserved_admin_username()
    return text


def new_password_failure(new_password, repeat_password):
    if new_password is None or len(new_password) < 1:
        return EMPTY_NEW_PASSWORD
    if new_password != repeat_password:
        return "Пароли не совпадают"
    return None


def cabinet_password_failure(stored, current_password, new_password, repeat_password):
    if not dbh.password_matches(current_password or "", stored):
        return WRONG_CURRENT_PASSWORD
    return new_password_failure(new_password, repeat_password)


def load_local_env():
    # .env из корня, уже заданные переменные не затираю
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


def registration_failure(code, username=""):
    # RESERVED_ADMIN код не проверяет
    if is_reserved_admin(username):
        return None
    load_local_env()
    expected = os.environ.get(REGISTRATION_CODE_ENV, "").strip()
    if not expected:
        return "Регистрация недоступна: не задан код регистрации"
    if code != expected:
        return "Неправильный код регистрации"
    return None


def registration_teacher_failure(teachers):
    if not teachers:
        return "Преподаватель не найден в справочнике"
    if len(teachers) > 1:
        return "В справочнике несколько преподавателей с таким ФИО"
    return None


def resolve_registration_teacher(username, last_name, first_name, middle_name):
    # обычно нужно ровно одно ФИО; для RESERVED_ADMIN карточку создаю, если её нет
    teachers = dbh.select_teacher_by_name(last_name, first_name, middle_name)
    if is_reserved_admin(username):
        if not teachers:
            dbh.insert_teacher(last_name, first_name, middle_name, "", "", None, "")
            teachers = dbh.select_teacher_by_name(last_name, first_name, middle_name)
        if not teachers:
            return None, f"Не удалось добавить преподавателя для {reserved_admin_username()}"
        return teachers[0][0], None
    failure = registration_teacher_failure(teachers)
    if failure:
        return None, failure
    return teachers[0][0], None


class AppearanceDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.success = False
        self.user = None
        self._place_auth_fields()
        for button in (
            self.ui.authPagePushButton,
            self.ui.regPagePushButton,
            self.ui.recoverPagePushButton,
        ):
            button.setCheckable(True)
            button.setAutoExclusive(True)
        self.setStyleSheet(
            self.styleSheet()
            + "QPushButton:checked {"
            " background-color: rgba(255, 255, 255, 45);"
            " border: 1px solid white;"
            "}"
        )
        self.go_to_auth()

        self.ui.authPagePushButton.clicked.connect(self.go_to_auth)
        self.ui.regPagePushButton.clicked.connect(self.go_to_register)
        self.ui.recoverPagePushButton.clicked.connect(self.go_to_recover)

        self.ui.authPushButton.clicked.connect(self.check_login)
        self.ui.registerButton.clicked.connect(self.register_user)
        self.ui.recoverPushButton.clicked.connect(self.check_recover)

    def _place_auth_fields(self):
        self.ui.label.setGeometry(10, 30, 121, 21)
        self.ui.authUsernameLine.setGeometry(140, 26, 211, 31)
        self.ui.label_3.setGeometry(10, 80, 121, 21)
        self.ui.authPassLine.setGeometry(140, 76, 211, 31)
        self.ui.authPushButton.setGeometry(110, 140, 181, 31)
        self.ui.checkBox.setGeometry(140, 184, 161, 20)
        self.ui.label_7.setText("Фамилия")
        self.ui.label_7.setGeometry(10, 140, 121, 21)
        self.ui.familiaLine.setGeometry(150, 136, 211, 31)
        self.ui.label_6.setText("Имя")
        self.ui.label_6.setGeometry(10, 180, 121, 21)
        self.ui.nameLine.setGeometry(150, 176, 211, 31)
        self.ui.label_11.setGeometry(10, 20, 121, 21)
        self.ui.recoverUsernameLine.setGeometry(150, 16, 211, 31)
        self.ui.label_12.setGeometry(10, 60, 131, 21)
        self.ui.revocerRegisterCodeLine.setGeometry(150, 56, 211, 31)
        self.ui.label_13.setText("Новый пароль")
        self.ui.label_13.setGeometry(10, 100, 121, 21)
        self.ui.recoverPassLine.setGeometry(150, 96, 211, 31)
        self.ui.label_14.setText("Повторите пароль")
        self.ui.label_14.setGeometry(10, 140, 131, 21)
        self.ui.recoverRepeatPassLine.setGeometry(150, 136, 211, 31)
        self.ui.recoverPushButton.setGeometry(110, 190, 181, 31)

    def go_to_auth(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)
        self.ui.mainInfoLabel.setText("Авторизация")
        self.setWindowTitle("Авторизация")
        self.ui.authPagePushButton.setChecked(True)

    def go_to_register(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
        self.ui.mainInfoLabel.setText("Регистрация")
        self.setWindowTitle("Регистрация")
        self.ui.regPagePushButton.setChecked(True)

    def go_to_recover(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_3)
        self.ui.mainInfoLabel.setText("Восстановление")
        self.setWindowTitle("Восстановление")
        self.ui.recoverPagePushButton.setChecked(True)

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
            try:
                save_remembered_username(username)
            except OSError as exc:
                QMessageBox.warning(self, "Ошибка", f"Не удалось запомнить вход: {exc}")
        self.success = True
        self.user = username
        self.accept()

    def register_user(self):
        username = canonical_username(self.ui.regUsernamLine.text())
        password = self.ui.regPassLine.text()
        password_rep = self.ui.regRepeatPassLine.text()
        name = self.ui.nameLine.text().strip()
        sec_name = self.ui.familiaLine.text().strip()
        middle_name = self.ui.otchestvoLine.text().strip()
        reg_code = self.ui.regCodeLine.text().strip()
        failure = registration_failure(reg_code, username)
        if failure:
            QMessageBox.warning(self, "Ошибка", failure)
            return
        if not password == password_rep:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
            return
        required = [username, password, name, sec_name, middle_name]
        if not is_reserved_admin(username):
            required.append(reg_code)
        if not all(required):
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните обязательные поля.")
            return
        try:
            teacher_id, failure = resolve_registration_teacher(
                username, sec_name, name, middle_name
            )
        except sqlite3.Error as exc:
            QMessageBox.warning(self, "Ошибка", f"Не удалось проверить преподавателя: {exc}")
            return
        if failure:
            QMessageBox.warning(self, "Ошибка", failure)
            return
        try:
            dbh.insert_user(teacher_id, username, password, sec_name, name, middle_name)
        except sqlite3.IntegrityError:
            if is_reserved_admin(username):
                QMessageBox.warning(
                    self,
                    "Ошибка",
                    f"Пользователь {reserved_admin_username()} уже зарегистрирован. "
                    "Войдите под этим именем.",
                )
                return
            QMessageBox.warning(
                self,
                "Ошибка",
                "Не удалось зарегистрировать пользователя. Попробуйте другое имя.",
            )
            return
        except sqlite3.Error as exc:
            QMessageBox.warning(
                self,
                "Ошибка",
                f"Не удалось зарегистрировать пользователя. Попробуйте другое имя: {exc}",
            )
            return
        QMessageBox.information(self, "Успешно", "Пользователь зарегистрирован")

    def check_recover(self):
        username = self.ui.recoverUsernameLine.text().strip()
        recoverCode = self.ui.revocerRegisterCodeLine.text().strip()
        password = self.ui.recoverPassLine.text()
        repeat_password = self.ui.recoverRepeatPassLine.text()
        if not all([username, recoverCode, password, repeat_password]):
            QMessageBox.warning(self, "Ошибка", "Заполните все поля.")
            return
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
        failure = new_password_failure(password, repeat_password)
        if failure:
            QMessageBox.warning(self, "Ошибка", failure)
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
