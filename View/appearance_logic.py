from PySide6.QtWidgets import QDialog, QMessageBox
from View.appearance import Ui_Dialog

# from passlib.hash import bcrypt  # returns when passwords are stored as hashes
import Models.dbhandler_new as dbh

SECRET_REG_CODE_HASH = "секрет123"


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

    def is_valid_registration_code(self, code: str) -> bool:
        return code == SECRET_REG_CODE_HASH

    def check_login(self):
        username = self.ui.authUsernameLine.text()
        password = self.ui.authPassLine.text()
        try:
            user = dbh.select_user_by_username(username)[0]
        except Exception:
            QMessageBox.warning(self, "Ошибка", "Неправильный логин")
            return
        if username == user[2] and password == user[3]:
            if self.ui.checkBox.isChecked():
                dbh.update_remember_status(username, 1)
            self.success = True
            self.user = username
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Неправильный пароль")
            return

    def register_user(self):
        username = self.ui.regUsernamLine.text()
        password = self.ui.regPassLine.text()
        password_rep = self.ui.regRepeatPassLine.text()
        name = self.ui.nameLine.text()
        sec_name = self.ui.familiaLine.text()
        middle_name = self.ui.otchestvoLine.text()
        reg_code = self.ui.regCodeLine.text()
        if not self.is_valid_registration_code(reg_code):
            return
        if not password == password_rep:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
            return
        if not all([username, password, name, sec_name, middle_name, reg_code]):
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните обязательные поля.")
            return
        try:
            teacher = dbh.select_teacher_by_name(sec_name, name, middle_name)[0]
            teacher_id = teacher[0]
        except Exception:
            teacher_id = ""
        try:
            dbh.insert_user(teacher_id, username, password, sec_name, name, middle_name)
        except Exception:
            QMessageBox.warning(
                self, "Ошибка", "Что-то пошло не так. Попробуйте поменять имя пользователя"
            )
        QMessageBox.information(self, "Успешно", "Пользователь зарегистрирован")

    def check_recover(self):
        username = self.ui.recoverUsernameLine.text()
        recoverCode = self.ui.revocerRegisterCodeLine.text()
        password = self.ui.recoverPassLine.text()
        repeat_password = self.ui.recoverRepeatPassLine.text()
        try:
            dbh.select_user_by_username(username)[0]
        except Exception:
            QMessageBox.warning(self, "Ошибка", "Неправильный логин")
            return
        if not self.is_valid_registration_code(recoverCode):
            QMessageBox.warning(self, "Ошибка", "Что-то пошло не так. Неправильный код регистрации")
            return
        if not password == repeat_password:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
            return
        try:
            dbh.update_user_password(username, password)
            QMessageBox.information(self, "Успешно", "Успешная смена пароля")
        except Exception:
            QMessageBox.warning(self, "Ошибка", "Что-то пошло не так")
            return

    def get_username(self):
        return self.user

    def get_success_status(self):
        return self.success
