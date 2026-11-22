import sqlite3
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox

import Models.dbhandler as dbh
from Models.model import PlanTableModel
from View.appearance_logic import (
    AppearanceDialog,
    cabinet_password_failure,
    new_password_failure,
)
from View.database_page import DatabasePage
from View.plan_page import PlanPage
from View.report_page import ReportPage
from View.workspace import Ui_MainWindow
from window_support import (
    OTCHET_TABLE_START_ROWS,
    ask_text,
    clear_remembered_username,
    help_path,
    prepare_table,
    read_remembered_username,
    saves_filename,
    split_expired_documents,
)

__all__ = ["OTCHET_TABLE_START_ROWS", "saves_filename", "split_expired_documents"]


def remembered_username():
    username = read_remembered_username()
    if not username:
        return None
    try:
        rows = dbh.select_user_by_username(username)
    except sqlite3.Error as exc:
        QMessageBox.warning(None, "Ошибка", f"Не удалось прочитать базу: {exc}")
        return None
    if not rows:
        return None
    return username


class MainWindow(DatabasePage, PlanPage, ReportPage, QMainWindow):
    def __init__(self, user=None):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Ведение документации по практикам")
        self.ui.otch_lbl_page_info.setText("Генерация отчёта")
        self.setStyleSheet(self.styleSheet() + "\nQPushButton { text-align: center; }\n")
        self._setup_navigation()
        self._setup_readable_buttons()
        self._setup_cabinet_fields()

        self.load_help_html()

        # Создаем базы данных
        try:
            dbh.create_tables()
        except sqlite3.Error as exc:
            QMessageBox.warning(self, "Ошибка", str(exc))
            self._startup_failed = True
            self.close()
            return

        self.user = user
        self._table_loaded = False
        self._nagruzka_loaded = False
        self._retention_reviewed = False

        self._db_model = None

        self._oth_frst_stg_model = None
        self._oth_scnd_std_model = None
        self._oth_thrd_stg_model = None
        self._fourth_stg_model = None
        self._fiveth_stg_model = None
        self._sixth_stg_model = None

        self._plan_data = None
        self._plan_headers = [
            "id",
            "№\nгруппы",
            "Вид практики\n(число студентов)",
            "Сроки\nпроведения\n(часы)",
            "Место\nпроведения\n(предприятие,\nкафедра)",
            "№\nдоговора",
            "Руководитель\nот университета\n(ФИО, должность,\nзвание, телефон)",
            "Руководитель\nот предприятия\n(ФИО, должность,\nтелефон)",
            "Специальность\nи шифр",
            "Необходимость\nзакупки\n(есть, нет)",
            "Примечание",
        ]
        self._plan_model = PlanTableModel(self._plan_data, self._plan_headers)
        self.ui.tableView.setModel(self._plan_model)
        prepare_table(self.ui.tableView, hide=(0,))
        # Определяем заголовки для таблиц
        self.set_otchet_tables_models()
        # Тут страница отчета
        self.ui.otch_prev_btn.clicked.connect(self.to_prev_stage)
        self.ui.otch_next_btn.clicked.connect(self.to_next_stage)
        self.ui.otch_pln_btn.clicked.connect(self.load_plan)
        self.ui.otchSaveAsPushButton.clicked.connect(self.save_otchet_as)
        self.ui.otchSavePushButton.clicked.connect(self.save_otchet)
        self.ui.pushButton.clicked.connect(self.load_saved_otchet)
        # first stage
        self.ui.meeting_date_otch_btn.clicked.connect(self.add_meting_date)
        # second stage
        self.ui.otchSecondStagePushButton.clicked.connect(self.otch_make_all_came)
        # third stage
        self.ui.otchOneRukVsemButton.clicked.connect(self.otch_all_ruk_vsem)
        # fourth stage
        self.ui.otchAllAnotherButton.clicked.connect(self.otch_refresh_drugoe)
        # sixth stage
        self.ui.otchAllUdlButton.clicked.connect(self.otch_vsem_three)
        self.ui.otchAllXorButton.clicked.connect(self.otch_vsem_four)
        self.ui.otchAllOtlButton.clicked.connect(self.otch_vsem_five)

        # Тут страница плана
        self.ui.loadTableButton.clicked.connect(self.load_table_new)
        self.ui.loadNagruzkaButton.clicked.connect(self.load_nagruzka)
        self.ui.loadPlanPushButton.clicked.connect(self.load_saved_plan)
        # проверяю insert rows для модели
        self.ui.notePlanPushButton.clicked.connect(self.open_group_dialog)
        # проверяю добавление значений
        self.ui.placePlanButton.clicked.connect(self.open_group_dialog)
        self.ui.agreementPlanPushButton.clicked.connect(self.open_group_dialog)
        self.ui.zakupkaPlanPushButton.clicked.connect(self.open_group_dialog)
        # проверяю диалоговое окно
        self.ui.rukPlanPushButton.clicked.connect(self.open_group_dialog)
        # работаем надо сохранениями
        self.ui.savePlanButton.clicked.connect(self.save_plan_new)
        self.ui.saveAsPlanButton.clicked.connect(self.save_plan_as)

        # Переключение между окнами
        self.ui.cabinetToolButton.clicked.connect(self.go_to_lk)
        self.ui.dataToolButton.clicked.connect(lambda: self.switch_page(0))
        self.ui.genOtchToolButton.clicked.connect(lambda: self.switch_page(1))
        self.ui.genPlanToolButton.clicked.connect(lambda: self.switch_page(2))
        self.ui.faqToolButton.clicked.connect(lambda: self.switch_page(3))
        self.ui.exitToolButton.clicked.connect(self.exit_function)

        # страница базы данных
        self.ui.dbPlansPushButton.clicked.connect(self.upload_db_docs)
        self.ui.dbPrepodsPushButton.clicked.connect(self.upload_db_teachers)
        self.ui.dbStarostaPushButton.clicked.connect(self.upload_db_starosta)

        self.ui.dbAddPrepodPushButton.clicked.connect(self.add_db_prepod)
        self.ui.dbEditPrepodPushButton.clicked.connect(self.edit_db_prepod)
        self.ui.dbDelPrepodPushButton.clicked.connect(self.remove_db_prepod)

        self.ui.dbAddStarostaPushButton.clicked.connect(self.add_db_starosta)
        self.ui.dbEditStarostaPushButton.clicked.connect(self.edit_db_starosta)
        self.ui.dbDelStarostaPushButton.clicked.connect(self.remove_db_starosta)

        self.ui.delDocumentPushButton.clicked.connect(self.remove_document)
        self.ui.defendDocumentPushButton.clicked.connect(self.defend_doucment)
        self.ui.openDocumentPushButton.clicked.connect(self.open_document)

        # страница личного кабинта
        self.ui.lkChangePassPushButton.clicked.connect(self.lk_change_password)
        self.ui.lkDelAccPushButton.clicked.connect(self.lk_del_account)
        self._nav_by_index[1].setChecked(True)
        self._update_stage_buttons()

    def _setup_navigation(self):
        style = (
            "QToolButton {"
            " color: white; font-size: 11pt; background-color: transparent;"
            " border: none; border-radius: 8px; font-family: Consolas; padding: 4px;"
            "}"
            "QToolButton:hover { background-color: rgba(255, 255, 255, 28); }"
            "QToolButton:checked {"
            " background-color: rgba(255, 255, 255, 48);"
            " border: 1px solid rgba(255, 255, 255, 90);"
            "}"
        )
        labels = (
            (self.ui.cabinetToolButton, "Личный кабинет"),
            (self.ui.dataToolButton, "База данных"),
            (self.ui.genOtchToolButton, "Генерация отчёта"),
            (self.ui.genPlanToolButton, "План"),
            (self.ui.faqToolButton, "Руководство"),
            (self.ui.exitToolButton, "Выйти"),
        )
        for button, text in labels:
            button.setStyleSheet(style)
            button.setText(text)
            button.setMinimumSize(188, 84)
        self._nav_by_index = {
            0: self.ui.dataToolButton,
            1: self.ui.genOtchToolButton,
            2: self.ui.genPlanToolButton,
            3: self.ui.faqToolButton,
            4: self.ui.cabinetToolButton,
        }
        for button in self._nav_by_index.values():
            button.setCheckable(True)
            button.setAutoExclusive(True)

    def _setup_readable_buttons(self):
        labels = {
            self.ui.dbAddPrepodPushButton: "Добавить преподавателя",
            self.ui.dbEditPrepodPushButton: "Изменить преподавателя",
            self.ui.dbDelPrepodPushButton: "Удалить преподавателя",
            self.ui.dbAddStarostaPushButton: "Добавить старосту",
            self.ui.dbEditStarostaPushButton: "Изменить старосту",
            self.ui.dbDelStarostaPushButton: "Удалить старосту",
            self.ui.otchAllAnotherButton: "Другое: как прибыло",
        }
        for button, text in labels.items():
            button.setText(text)
            button.setMinimumHeight(36)
            button.setMaximumWidth(16777215)
        centered = (
            self.ui.dbAddPrepodPushButton,
            self.ui.dbEditPrepodPushButton,
            self.ui.dbDelPrepodPushButton,
            self.ui.dbAddStarostaPushButton,
            self.ui.dbEditStarostaPushButton,
            self.ui.dbDelStarostaPushButton,
            self.ui.otchAllAnotherButton,
            self.ui.meeting_date_otch_btn,
            self.ui.otchSecondStagePushButton,
            self.ui.otchOneRukVsemButton,
            self.ui.otchAllUdlButton,
            self.ui.otchAllXorButton,
            self.ui.otchAllOtlButton,
        )
        for button in centered:
            button.setStyleSheet(
                "QPushButton { color: white; text-align: center; }"
                "QPushButton:disabled {"
                " color: rgba(255, 255, 255, 0.4);"
                " background-color: rgba(155, 79, 165, 70);"
                "}"
            )

    def _setup_cabinet_fields(self):
        style = (
            "QLineEdit {"
            " background-color: transparent;"
            " border: none;"
            " border-bottom: 1px solid rgba(255, 255, 255, 50);"
            " color: white;"
            " padding: 4px 8px;"
            "}"
        )
        fields = (
            self.ui.lkUsernameLine,
            self.ui.lkLastNameLine,
            self.ui.lkNameLine,
            self.ui.lkMiddleNameLine,
            self.ui.lkTitleLine,
            self.ui.lkDegreeLine,
            self.ui.lkEmailLine,
            self.ui.lkPhoneLine,
        )
        for field in fields:
            field.setStyleSheet(style)
            field.setPlaceholderText("не указано")
        self.ui.lkDelAccPushButton.setGeometry(490, 220, 191, 31)

    def load_help_html(self):
        with open(help_path, "r", encoding="utf-8") as f:
            html = f.read()
        self.ui.faqTextBrowser.setHtml(html)

    def lk_del_account(self):
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Вы уверены, что хотите удалить этот аккаунт?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,  # По умолчанию выделена кнопка "Нет"
        )

        if reply == QMessageBox.Yes:
            # Действие при подтверждении
            dbh.remove_user(self.user)
            self.exit_function()
        else:
            # Отмена действия
            return

    def lk_change_password(self):
        password = self.ui.lkNewPassLine.text()
        repeat_password = self.ui.lkRepeatPassLine.text()
        failure = new_password_failure(password, repeat_password)
        if failure:
            QMessageBox.warning(self, "Ошибка", failure)
            return
        current_password = ask_text(self, "Смена пароля", "Текущий пароль:", password=True)
        if current_password is None:
            return
        try:
            users = dbh.select_user_by_username(self.user)
        except sqlite3.Error as exc:
            QMessageBox.warning(self, "Ошибка", f"Не удалось проверить учётную запись: {exc}")
            return
        if not users:
            QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
            return
        failure = cabinet_password_failure(users[0][3], current_password, password, repeat_password)
        if failure:
            QMessageBox.warning(self, "Ошибка", failure)
            return
        try:
            dbh.update_user_password(self.user, password)
        except sqlite3.Error as exc:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сменить пароль: {exc}")
            return
        QMessageBox.information(self, "Успешно", "Успешная смена пароля")

    def go_to_lk(self):
        try:
            users = dbh.select_user_by_username(self.user)
        except sqlite3.Error as exc:
            QMessageBox.warning(self, "Ошибка", f"Не удалось открыть кабинет: {exc}")
            return
        if not users:
            QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
            return
        user = users[0]
        try:
            teachers = dbh.select_teacher_by_id(user[1])
        except sqlite3.Error as exc:
            QMessageBox.warning(self, "Ошибка", f"Не удалось открыть кабинет: {exc}")
            return
        if not teachers:
            QMessageBox.warning(self, "Ошибка", "Преподаватель не найден в справочнике")
            return
        user_data = teachers[0]
        self.switch_page(4)
        self.ui.lkUsernameLine.setText(self.user)
        self.ui.lkLastNameLine.setText(user[4])
        self.ui.lkNameLine.setText(user[5])
        self.ui.lkMiddleNameLine.setText(user[6])
        self.ui.lkTitleLine.setText(user_data[5])
        self.ui.lkDegreeLine.setText(user_data[4])
        self.ui.lkEmailLine.setText(user_data[-2])
        self.ui.lkPhoneLine.setText(user_data[-1])

    def switch_page(self, index):
        self.ui.mainStackedWidget.setCurrentIndex(index)
        button = self._nav_by_index.get(index)
        if button is not None:
            button.setChecked(True)
        if index == 0:
            self.upload_db_docs(review_retention=not self._retention_reviewed)

    def exit_function(self):
        clear_remembered_username()
        self.restart_auth = True
        self.close()  # просто закрываем окно, не sys.exit()


def run_application():
    while True:
        # 1. Проверка, запомнен ли пользователь
        username = remembered_username()
        if username is None:
            appearance = AppearanceDialog()
            appearance.exec()
            if not appearance.get_success_status():
                break
            username = appearance.get_username()

        # 3. Запускаем основное окно
        main_window = MainWindow(user=username)
        if getattr(main_window, "_startup_failed", False):
            break
        main_window.show()

        # 4. Запускаем event loop и ждём выхода
        app.exec()

        # 5. Если внутри MainWindow вызвали "выход" и закрыли — продолжаем с начала
        if getattr(main_window, "restart_auth", False):
            continue
        else:
            break  # обычный выход, завершаем


if __name__ == "__main__":
    app = QApplication(sys.argv)
    run_application()
