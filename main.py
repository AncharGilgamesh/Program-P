import sqlite3
import sys

from PySide6.QtWidgets import QApplication, QHeaderView, QMainWindow, QMessageBox

import Models.dbhandler as dbh
from Models.model import PlanTableModel
from View.appearance_logic import AppearanceDialog
from View.database_page import DatabasePage
from View.plan_page import PlanPage
from View.report_page import ReportPage
from View.workspace import Ui_MainWindow
from window_support import (
    OTCHET_TABLE_START_ROWS,
    help_path,
    saves_filename,
    split_expired_documents,
)

__all__ = ["OTCHET_TABLE_START_ROWS", "saves_filename", "split_expired_documents"]


def remembered_username():
    """Логин с включённым «запомнить меня». Пустой список — не ошибка."""
    try:
        rows = dbh.select_remembered_user()
    except sqlite3.Error as exc:
        QMessageBox.warning(None, "Ошибка", f"Не удалось прочитать базу: {exc}")
        return None
    if not rows or not rows[0] or not rows[0][3]:
        return None
    return rows[0][2]


class MainWindow(DatabasePage, PlanPage, ReportPage, QMainWindow):
    def __init__(self, user=None):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.load_help_html()

        # Создаем базы данных
        dbh.create_tables()

        self.user = user
        self._table_loaded = False
        self._nagruzka_loaded = False

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
            "№\nгр.",
            "Вид практики\n(кол-во студентов)",
            "Сроки\nпроведения\n(кол-во часов)",
            "Место\nпроведения\n(предприятие, кафедра)",
            "№ договора\nс предприя-\nтием\n(числа)",
            "Руководитель от\nуниверситета(ф.и.о.,\nдолжность, звание,\n контактный тел.)",
            "Руководитель от\nпредпр-я(ф.и.о.,\nдолж.,контакт.\nТел.)",
            "Наименование\nспециальности и ее\nшифр",
            "Необходимо\nсть закупки\n(есть, нет)",
            "Примечан\nие",
        ]
        self._plan_model = PlanTableModel(self._plan_data, self._plan_headers)
        self.ui.tableView.setModel(self._plan_model)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.tableView.hideColumn(0)
        # Определяем заголовки для таблиц
        self.set_otchet_tables_models()
        # Тут страница отчета
        self.ui.otch_prev_btn.clicked.connect(self.to_prev_stage)
        self.ui.otch_next_btn.clicked.connect(self.to_next_stage)
        self.ui.otch_pln_btn.clicked.connect(self.load_plan)
        self.ui.otchSaveAsPushButton.clicked.connect(self.save_otchet_as)
        self.ui.otchSavePushButton.clicked.connect(self.save_otchet)
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
        if not password == repeat_password:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают")
            return

        try:
            dbh.update_user_password(self.user, password)
        except sqlite3.Error as exc:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сменить пароль: {exc}")
            return
        QMessageBox.information(self, "Успешно", "Успешная смена пароля")

    def go_to_lk(self):
        self.switch_page(4)
        user = dbh.select_user_by_username(self.user)[0]
        # передаем teacher_id, чтобы получить инфу по преподавателю
        user_data = dbh.select_teacher_by_id(user[1])[0]
        self.ui.lkUsernameLine.setText(self.user)
        self.ui.lkLastNameLine.setText(user[4])
        self.ui.lkNameLine.setText(user[5])
        self.ui.lkMiddleNameLine.setText(user[6])
        self.ui.lkTitleLine.setText(user_data[5])
        self.ui.lkDegreeLine.setText(user_data[4])
        self.ui.lkEmailLine.setText(user_data[-2])
        self.ui.lkPhoneLine.setText(user_data[-1])

    def switch_page(self, index):
        """Переключает страницу в QStackedWidget и обновляет состояние кнопок"""
        self.ui.mainStackedWidget.setCurrentIndex(index)
        if index == 0:
            self.upload_db_docs(review_retention=True)

    def exit_function(self):
        dbh.update_remember_status(self.user, 0)
        self.restart_auth = True
        self.close()  # просто закрываем окно, не sys.exit()


def check_for_appearance():
    username = remembered_username()
    if username:
        return username
    appearance = AppearanceDialog()
    appearance.exec()
    if not appearance.get_success_status():
        sys.exit()
    return appearance.get_username()


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
    """
    username = check_for_appearance()
    window = MainWindow(user=username)
    window.show()

    sys.exit(app.exec())"""
