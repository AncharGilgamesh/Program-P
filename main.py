import sys
import datetime
import os
import platform
import subprocess

import pandas as pd
import Models.datahandler as dh
import Models.dbhandler_new as dbh
from docx import Document
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QHeaderView, QMessageBox, QInputDialog
from PySide6.QtCore import QSortFilterProxyModel, Qt


from Models.model import PlanTableModel, ResultTableModel

from View.workspace import Ui_MainWindow
from View.appearance_logic import AppearanceDialog
from View.planaddingdialogs import GroupEditDialog
from View.smartTableView import SmartTableView
from View.meetingdatedialog import MeetingDateDialog
from View.prepod_dialog import PrepodDialog
from View.startosta_dialog import StarostaDialog

base_dir = os.path.dirname(os.path.abspath(__file__))
help_path = os.path.join(base_dir, "", "help.html")
shablon_plan_path = os.path.join(base_dir, "Shablons", "shablon_plan.docx" )
shablon_otch_path = os.path.join(base_dir, "Shablons", "shablon_otchet.docx" )

class MainWindow(QMainWindow):
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
            "№\nгр.", "Вид практики\n(кол-во студентов)", "Сроки\nпроведения\n(кол-во часов)", "Место\nпроведения\n(предприятие, кафедра)",
            "№ договора\nс предприя-\nтием\n(числа)","Руководитель от\nуниверситета(ф.и.о.,\nдолжность, звание,\n контактный тел.)",
            "Руководитель от\nпредпр-я(ф.и.о.,\nдолж.,контакт.\nТел.)", "Наименование\nспециальности и ее\nшифр",
              "Необходимо\nсть закупки\n(есть, нет)", "Примечан\nие"]
        self._plan_model = PlanTableModel(self._plan_data, self._plan_headers)
        self.ui.tableView.setModel(self._plan_model)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.tableView.hideColumn(0)
        # Определяем заголовки для таблиц
        self.set_otchet_tables_models()
        # Новый участок кода
        """
        Этот участок кода реализует поиск в таблице. Пока не знаю. нужно ли это вообще мне
        self.proxy_model = QSortFilterProxyModel(self)
        self.proxy_model.setSourceModel(self._plan_model)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.proxy_model.setFilterKeyColumn(-1)  # по умолчанию — все столбцы
        self.ui.tableView.setModel(self.proxy_model)
        self.ui.planSearchComboBox.addItem("Все столбцы", -1)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.tableView.hideColumn(0)
        for i in range(self._plan_model.columnCount()):
            header = self._plan_model.headerData(i, Qt.Horizontal)
            self.ui.planSearchComboBox.addItem(header, i)
        # Сигналы
        self.ui.searchPlanLineEdit.textChanged.connect(self.apply_filter)
        self.ui.planSearchComboBox.currentIndexChanged.connect(self.apply_filter)
        #Конец нового участка кода
        """
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

    # ==========================Код для работы с личным кабинетом ==========================================
    def lk_del_account(self):
        reply = QMessageBox.question(
            self, "Подтверждение",
            "Вы уверены, что хотите удалить этот аккаунт?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No  # По умолчанию выделена кнопка "Нет"
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
            QMessageBox.information(self, "Успешно", "Успешная смена пароля")
        except:
            QMessageBox.warning(self, "Ошибка", "Что-то пошло не так")
            return
    
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



    # ==========================Код для работы с базой данных===============================================
    def open_document(self):
        index = self.ui.dataBaseTableView.selectedIndexes()[0]
        row = index.row()
        data = self._db_model.get_row(row)
        file_path = data[-1]
        system = platform.system()
        if system == "Windows":
            os.startfile(file_path)  # Самый простой способ для Windows
        elif system == "Darwin":     # macOS
            subprocess.run(["open", file_path])
        else:                        # Linux и другие
            subprocess.run(["xdg-open", file_path])

    def defend_doucment(self):
        index = self.ui.dataBaseTableView.selectedIndexes()[0]
        row = index.row()
        data = self._db_model.get_row(row)
        id = data[0]
        if data[-2] == 0:
            dbh.defend_document(id, 1)
        else:
            dbh.defend_document(id, 0)
        self.upload_db_docs()

    
    def remove_document(self):
        index = self.ui.dataBaseTableView.selectedIndexes()[0]
        row = index.row()
        data = self._db_model.get_row(row)
        id = data[0]
        try:
            dbh.remove_document(id)
            os.remove(data[-1])
            self.upload_db_docs()
        except:
            return


    def upload_db_starosta(self):
        self.ui.dbPageStackedWidget.setCurrentIndex(1)
        data = dbh.load_starostas()
        headers = ["id","id_Куратора", "Фамилия", "Имя", "Отчество", "Группа", "Почта", "Номер"]
        self._db_model = PlanTableModel(data, headers)
        self.ui.dataBaseTableView.setModel(self._db_model)

    def add_db_starosta(self):
        teachers = dbh.load_teachers()
        dialog = StarostaDialog(teachers=teachers, parent=self)
        if dialog.exec():
            data = dialog.get_data()
        try:
            dbh.insert_starosta(*data)
            self.upload_db_starosta()
        except:
            return
        
    def edit_db_starosta(self):
        teachers = dbh.load_teachers()
        index = self.ui.dataBaseTableView.selectedIndexes()[0]
        row = index.row()
        data = self._db_model.get_row(row)
        id = data[0]
        dialog = StarostaDialog(teachers=teachers, starosta_data=list(data[1:]), parent=self)
        if dialog.exec():
            data = dialog.get_data()
        try:
            dbh.update_starosta(id, data)
            self.upload_db_starosta()
        except:
            return

    def remove_db_starosta(self):
        index = self.ui.dataBaseTableView.selectedIndexes()[0]
        row = index.row()
        data = self._db_model.get_row(row)
        id = data[0]
        try:
            dbh.remove_starosta(id)
            self.upload_db_starosta()
        except:
            return


    def upload_db_teachers(self):
        self.ui.dbPageStackedWidget.setCurrentIndex(0)
        data = dbh.load_teachers()
        headers = ["id", "Фамилия", "Имя", "Отчество", "Степень", "Должность", "Почта", "Номер"]
        self._db_model = PlanTableModel(data, headers)
        self.ui.dataBaseTableView.setModel(self._db_model)
        

    def add_db_prepod(self):
        dialog = PrepodDialog(parent=self)
        if dialog.exec():
            data = dialog.get_data()
        try:
            dbh.insert_teacher(*data)
            self.upload_db_teachers()
        except:
            return

    def edit_db_prepod(self):
        index = self.ui.dataBaseTableView.selectedIndexes()[0]
        row = index.row()
        data = self._db_model.get_row(row)
        id = data[0]
        dialog = PrepodDialog(data=data[1:], parent=self)
        if dialog.exec():
            data = dialog.get_data()
        try:
            dbh.update_teacher(id, data)
            self.upload_db_teachers()
        except:
            return

    def remove_db_prepod(self):
        index = self.ui.dataBaseTableView.selectedIndexes()[0]
        row = index.row()
        data = self._db_model.get_row(row)
        id = data[0]
        try:
            dbh.remove_teacher(id)
            self.upload_db_teachers()
        except:
            return


    def upload_db_docs(self):
        self.ui.dbPageStackedWidget.setCurrentIndex(2)
        data = dbh.load_docs()
        print(data)
        headers = ["id", "Год", "Тип", "Дата создания", "Создатель", "Защищено", "Путь"]
        self._db_model = PlanTableModel(data, headers)
        self.ui.dataBaseTableView.setModel(self._db_model)


    # ==========================Код для работы с отчетом====================================================
    def save_otchet_as(self):
        doc = Document(shablon_otch_path)
        data_for_save = []
        data_for_save.append(self._oth_frst_stg_model.get_data())
        data_for_save.append(self._oth_scnd_std_model.get_data())
        data_for_save.append(self._oth_thrd_stg_model.get_data())
        data_for_save.append(self._fourth_stg_model.get_data())
        data_for_save.append(self._fiveth_stg_model.get_data())
        data_for_save.append(self._sixth_stg_model.get_data())
        start_row = 2
        for i in range(len(data_for_save)):
            if i==0:
                start_row = 1
            if i==4:
                start_row = 5
            else:
                start_row = 2
            table = doc.tables[i]
            dh.fill_the_table_rows(table, data_for_save[i], start_row)
        options = QFileDialog.Options()
        fname, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить файл", "", "Word файлы (*.docx)", options=options)
        if not fname:
            return
        doc.save(fname)

    def save_otchet(self):
        year = datetime.datetime.now().year
        current_date = str(datetime.datetime.now().strftime("%Y.%m.%d"))
        doc = Document(shablon_otch_path)
        data_for_save = []
        data_for_save.append(self._oth_frst_stg_model.get_data())
        data_for_save.append(self._oth_scnd_std_model.get_data())
        data_for_save.append(self._oth_thrd_stg_model.get_data())
        data_for_save.append(self._fourth_stg_model.get_data())
        data_for_save.append(self._fiveth_stg_model.get_data())
        data_for_save.append(self._sixth_stg_model.get_data())
        start_row = 2
        for i in range(len(data_for_save)):
            if i==0:
                start_row = 1
            if i==4:
                start_row = 5
            else:
                start_row = 2
            table = doc.tables[i]
            dh.fill_the_table_rows(table, data_for_save[i], start_row)
        creator = self.user
        save_path = os.path.join(base_dir, "Saves", f"{year}_o.docx")
        dbh.insert_document(year,"Отчет", current_date, creator, save_path, 0)
        doc.save(f'Saves/{year}_o.docx')

    def otch_vsem_five(self):
       self._sixth_stg_model.fill_column_with_value(7, "+")
       self._sixth_stg_model.fill_column_with_value(6, "")
       self._sixth_stg_model.fill_column_with_value(5, "")

    def otch_vsem_four(self):
        self._sixth_stg_model.fill_column_with_value(7, "")
        self._sixth_stg_model.fill_column_with_value(6, "+")
        self._sixth_stg_model.fill_column_with_value(5, "")

    def otch_vsem_three(self):
        self._sixth_stg_model.fill_column_with_value(7, "")
        self._sixth_stg_model.fill_column_with_value(6, "")
        self._sixth_stg_model.fill_column_with_value(5, "+")

    def otch_refresh_drugoe(self):
        values = self._oth_scnd_std_model.get_col(4)
        self._fourth_stg_model.set_col(6, values)

    def otch_all_ruk_vsem(self):
        fio = show_fio_dialog(parent=self)  # Замените 'window' на вашу основную форму
        if fio:
            target_column = 2
            self._oth_thrd_stg_model.set_col(target_column, [fio] * self._oth_thrd_stg_model.rowCount())  # Вставить ФИО во все строки

    def otch_make_all_came(self):
        values = self._oth_scnd_std_model.get_col(3)
        self._oth_scnd_std_model.set_col(4, values)

    def set_otchet_resizing(self):
        self.ui.otchFirstTableView.resizeRowsToContents()
        self.ui.otchSecondTableView.resizeRowsToContents()
        self.ui.otchThirdTableView.resizeRowsToContents()
        self.ui.otchFourthTableView.resizeRowsToContents()

        self.ui.otchFivethTableView.resizeRowsToContents()
        self.ui.otchSixthTableView.resizeRowsToContents()


    def add_meting_date(self):
        data_for_meeting = self._oth_frst_stg_model.get_data()
        data_fin = dh.get_group_practice_keys_frst_stg(data_for_meeting)
        dialog = GroupEditDialog(data_fin, self)

        if dialog.exec():
            selected_keys, date_str = dialog.get_result()
            rows_to_update = dh.get_target_row_indices(data_for_meeting, selected_keys)
            # можно выделить это в отдельную функцию для добавления по индексам!!!!!!!!!
            for row in rows_to_update:
                # столбец 5 — это "Дата проведения собрания"
                self._oth_frst_stg_model.setData(self._oth_frst_stg_model.index(row, 5), date_str)
    # Переработал первый этап, эта функция будет пополняться по мере заполнения этапов
    def load_plan(self):
        fname, _ = QFileDialog.getOpenFileName(
            self, "Choose file", "", "Excel Files (*.docx)")
        if not fname:
            return
        data = dh.read_plan_from_docx(fname)
        # Вот эту функцию нужно переработать, чтобы даты не брались
        table1 = dh.parse_practice_table(data[1:])  # пропускаем заголовки
        self._oth_frst_stg_model.insertRows(0,len(table1), table1)
        table2 = dh.parse_second_table(data[1:])
        self._oth_scnd_std_model.insertRows(0, len(table2), table2)
        table3 = dh.parse_third_table(data[1:])
        self._oth_thrd_stg_model.insertRows(0, len(table3), table3)
        table4 = dh.parse_fourth_table(table2)
        self._fourth_stg_model.insertRows(0, len(table4), table4)

        table5 = dh.parse_fiveth_table(table2)
        self._fiveth_stg_model.insertRows(0, len(table5), table5)
        table6 = dh.parse_sixth_table(table1, data)
        self._sixth_stg_model.insertRows(0, len(table6), table6)
        self.set_otchet_resizing()
    
        #self._fourth_stg_model.insertRows(0, len(table4), table4)
        # вот тут представлены варианты изменения размера, нужно это все рассмотреть получше
        #self.ui.otchThirdTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.ui.otchThirdTableView.resizeRowsToContents()
        #Для четвертой таблицы попробуй взять инфу из второй таблицы и надо подредактировать
        #Сделать диалоговое окно, чтобы можно было заполнять таблицу из второй таблицы
            
    def to_next_stage(self):
        index = self.ui.stackedWidget.currentIndex()+1
        if index == 6:
            return
        self.ui.otch_lbl_stage.setText(f'{index + 1} этап')
        self.ui.stackedWidget.setCurrentIndex(index)

    def to_prev_stage(self):
        index = self.ui.stackedWidget.currentIndex()-1
        if index == -1:
            return
        self.ui.otch_lbl_stage.setText(f'{index + 1} этап')
        self.ui.stackedWidget.setCurrentIndex(index)

    def set_otchet_tables_models(self):
        headers_for_first_stage = [
            "№", "Группа", "Направление\n/Специальность", "Семестр", "Вид практики", "Дата\nпроведения\nсобрания"
            ]
        headers_for_second_stage = [
            "№\nп/п", "Город", "Место проведения", "Направлено", "Прибыло", "Инструктаж по ТБ", "Факт. конец"
        ]
        headers_for_third_stage = [
            "Место", "Рук. от КАИ", "Рук. от предприятия"
        ]
        headers_fourth_stage = [
            "Место\nпроведения\nпрактики", "В цехах", "Офис", "Инженерно-\nтехнические\nдолжности", "Научные\nлаборатории",
            "Студ.\n отряды", "Другое", "Оформление\nТБ на рабочем\nместе(да\нет)"
        ]
        headers_fiveth_stage = [
            "Группа", "Всего\nчел.", "Отл.", "Хор.", "Удовл.", "Неуд.", "Не\nзащитило", "Место\nзащиты"
        ]
        headers_sixth_stage = [
            "№", "Руководитель", "Должность", "Группа", "Вид\nпрактики", "Удовл.", "Хор.", "Отл."
        ]
        first_data = None
        self._oth_frst_stg_model = PlanTableModel(first_data, headers_for_first_stage)
        self.ui.otchFirstTableView.setModel(self._oth_frst_stg_model)
        self._oth_scnd_std_model = PlanTableModel(first_data, headers_for_second_stage)
        self.ui.otchSecondTableView.setModel(self._oth_scnd_std_model)
        self._oth_thrd_stg_model = PlanTableModel(first_data, headers_for_third_stage)
        self.ui.otchThirdTableView.setModel(self._oth_thrd_stg_model)
        self._fourth_stg_model = PlanTableModel(first_data, headers_fourth_stage)
        self.ui.otchFourthTableView.setModel(self._fourth_stg_model)
        self._fiveth_stg_model = ResultTableModel(first_data, headers_fiveth_stage)
        self.ui.otchFivethTableView.setModel(self._fiveth_stg_model)
        self._sixth_stg_model = PlanTableModel(first_data, headers_sixth_stage)
        self.ui.otchSixthTableView.setModel(self._sixth_stg_model)


    # Функция для переключения окон
    def switch_page(self, index):
        """Переключает страницу в QStackedWidget и обновляет состояние кнопок"""
        self.ui.mainStackedWidget.setCurrentIndex(index)
        if index == 0:
            self.upload_db_docs()
    # ==========================Код для работы с планом====================================================

    def save_plan_as(self):
        doc = Document(shablon_plan_path)
        data_for_save = self._plan_model.get_data_without_id()
        table = doc.tables[0]
        start_row = 2
        dh.fill_the_table_rows(table, data_for_save, start_row)
        options = QFileDialog.Options()
        fname, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить файл", "", "Excel файлы (*.docx)", options=options)
        if not fname:
            return
        doc.save(fname)

    def save_plan_new(self):
        year = datetime.datetime.now().year
        current_date = str(datetime.datetime.now().strftime("%Y.%m.%d"))
        doc = Document(shablon_plan_path)
        data_for_save = self._plan_model.get_data_without_id()
        table = doc.tables[0]
        start_row = 2
        dh.fill_the_table_rows(table, data_for_save, start_row)
        creator = self.user
        save_path = os.path.join(base_dir, "Saves", f"{year}_p.docx")
        dbh.insert_document(year,"План", current_date, creator, save_path, 0)
        doc.save(f'Saves/{year}_p.docx')
        
            
        

    # Модифицируем метод для открытия редактирования
    def open_group_dialog(self):
        """Этот метод используется в плане для редактирования столбцов"""
        self.button_to_keyword = {
            "Примечание": "Примечан",
            "Место проведения": "Место\nпроведения",
            "№ договора": "№ договора",
            "Необходимость закупки": "Необходимо",
            "Руководитель от предприятия": "Руководитель от\nпредпр-я",
        }
        button = self.sender()
        if not button:
            return
        field_label = button.text()
        title = "Добавление данных для столбца " + '"' + field_label + '"'
        all_group_names = self._plan_model.get_column_values(1)
        all_group_names = list(dict.fromkeys(all_group_names))
        dialog = GroupEditDialog(all_group_names, field_label=field_label, title=title, parent=self)
        keyword = self.button_to_keyword.get(field_label)
        if dialog.exec():
            selected_groups, value = dialog.get_result()
            # print(selected_groups, value)
            col = dh.find_column_index_by_keyword(self._plan_model, keyword)
            for group in selected_groups:
                self._plan_model.updateCellsByCondition(1, int(group), col, str(value))
                   

    def load_nagruzka(self):
        fname, _ = QFileDialog.getOpenFileName(
            self, "Choose file", "", "Excel Files (*.xlsx *.xls *.xlsm)")
        if not fname:
            return
        data = pd.read_excel(fname, header=None)
        extracted_data = dh.extract_data(data)
        if self._table_loaded:
            additional_data = dh.extract_additional_info_form_nagruzka(data)
            for key in additional_data.keys():
                self._plan_model.add_info_to_cell_by_condition(1, key, 2, additional_data[key])
        else:
            extracted_data = dh.extract_data(data)
            self._plan_model.insertRows(0, len(extracted_data), extracted_data)
        self._nagruzka_loaded = True
        self.ui.tableView.resizeRowsToContents()
        

    def load_table_new(self):
        fname, _ = QFileDialog.getOpenFileName(
            self, "Choose file", "", "Excel Files (*.xlsx *.xls *.xlsm)")
        if not fname:
            return
        baka = pd.read_excel(fname, 0, header=None)
        maga = pd.read_excel(fname, 1, header=None)
        #keywords = ["практика", "магистратура"]

        # Проход по всем ячейкам датафрейма
        """
        for row_idx, row in df.iterrows():
            for col in df.columns:
                value = str(row[col])
                for word in keywords:
                    if word.lower() in value.lower():
                        print(f"Найдено слово '{word}' в ячейке [{row_idx}, '{col}']: {value}")"""
        # Пример использования
        blocks = dh.extract_practice_blocks_with_empty_stop(baka)
        blocks_maga = dh.extract_practice_blocks_with_empty_stop(maga)

        # Вывод результатов
        
        #print(blocks_maga)
        blocks_baka_tr = dh.transform_practice_data(blocks)
        blocks_maga_tr = dh.transform_practice_data(blocks_maga, len(blocks_baka_tr))
        combined_blocks = blocks_baka_tr + blocks_maga_tr
        self._plan_model.insertRows(0, len(combined_blocks), combined_blocks)
        self._table_loaded = True
        self.ui.tableView.resizeRowsToContents()
        """
        for i, block in enumerate(blocks_maga, 1):
            print(f"\nБлок {i}:")
            print(f"Заголовок: {block['title']}")
            print("Данные:")
            block_df = pd.DataFrame(block['data'])
            print(block_df.to_string(index=False, header=False))"""

    def exit_function(self):
        dbh.update_remember_status(self.user, 0)
        self.restart_auth = True
        self.close()  # просто закрываем окно, не sys.exit()

def check_for_appearance():
    try:
        user = dbh.select_remembered_user()[0]
        if user:
            return user[2]
    except:
        appearance = AppearanceDialog()
        appearance.exec()
        if not appearance.get_success_status():
            sys.exit()
        return appearance.get_username()


def show_fio_dialog(parent=None):
        text, ok = QInputDialog.getText(parent, "Введите ФИО", "Фамилия и инициалы:")
        if ok and text.strip():
            return text.strip()
        return None

def run_application():
    while True:
        # 1. Проверка, запомнен ли пользователь
        try:
            user = dbh.select_remembered_user()[0]
            if user and user[3]:  # если есть флаг remember_me
                username = user[2]
            else:
                raise Exception("Требуется авторизация")
        except:
            # 2. Открываем окно авторизации
            appearance = AppearanceDialog()
            appearance.exec()
            if not appearance.get_success_status():
                break  # выход из цикла и завершение приложения
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
    '''
    username = check_for_appearance()
    window = MainWindow(user=username)
    window.show()

    sys.exit(app.exec())'''