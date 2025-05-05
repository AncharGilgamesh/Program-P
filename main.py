import sys
import datetime

import pandas as pd
import datahandler as dh
import Models.dbhandler_new as dbh
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QHeaderView
from PySide6.QtCore import QSortFilterProxyModel, Qt


from model import PlanTableModel, ResultTableModel

from View.workspace import Ui_MainWindow
from View.planaddingdialogs import GroupEditDialog
from View.smartTableView import SmartTableView
from View.meetingdatedialog import MeetingDateDialog
from View.prepod_dialog import PrepodDialog
from View.startosta_dialog import StarostaDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Создаем базы данных
        dbh.create_tables()

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
        # first stage
        self.ui.meeting_date_otch_btn.clicked.connect(self.add_meting_date)
        # Тут страница плана        
        self.ui.loadTableButton.clicked.connect(self.load_table_new)
        self.ui.loadNagruzkaButton.clicked.connect(self.fill_the_shablon)
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
        # Переключение между окнами
        self.ui.cabinetToolButton.clicked.connect(lambda: self.switch_page(4))
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



    # ==========================Код для работы с базой данных===============================================

    def upload_db_starosta(self):
        data = dbh.load_starostas()
        headers = ["id","id_Куратора", "Фамилия", "Имя", "Отчество", "Группа", "Почта", "Номер"]
        self._db_model = PlanTableModel(data, headers)
        self.ui.dataBaseTableView.setModel(self._db_model)

    def add_db_starosta(self):
        teachers = [
            (1, "Иванов", "Иван", "Иванович", ...),
            (2, "Петров", "Пётр", "Петрович", ...),
            (3, "Сидоров", "Сидор", "Сидорович", ...)
        ]
        dialog = StarostaDialog(teachers=teachers, parent=self)
        if dialog.exec():
            data = dialog.get_data()
        print(data)

    def upload_db_teachers(self):
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
        data = dbh.load_docs()
        headers = ["id", "Год", "Тип", "Дата создания", "Создатель", "Защищено", "Открыть"]
        self._db_model = PlanTableModel(data, headers)
        self.ui.dataBaseTableView.setModel(self._db_model)


    # ==========================Код для работы с отчетом====================================================

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
            "Группа", "Всего\nчел.", "Отл.", "Хор.", "Неуд.", "Не\nзащитило", "Место\nзащиты"
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
    # ==========================Код для работы с планом====================================================
    def save_plan_new(self):
        year = datetime.datetime.now().year
        current_date = str(datetime.datetime.now().strftime("%Y.%m.%d"))
        doc = Document("E:/Python/Magistr_Project/Test_results/shablon_plan.docx")
        data_for_save = self._plan_model.get_data_without_id()
        table = doc.tables[0]
        start_row = 2
        self.fill_the_table_rows(table, data_for_save, start_row)
        dbh.insert_document(year,"План", current_date, "Вася Пупкин", f"Saves/{year}.docx", False)
        doc.save(f'Saves/{year}.docx')
        


    # Реализуем обычное сохранение
    def save_plan_function(self):
        doc = Document("E:/Python/Magistr_Project/Test_results/shablon_plan.docx")
        data_for_save = self._plan_model.get_data_without_id()
        table = doc.tables[0]
        start_row = 2
        self.fill_the_table_rows(table, data_for_save, start_row)
        print("Сохранение успешно")
        doc.save("Test_results/plan_zapolnen.docx")


    # Открывает диалоговое окно с выбором групп и редактирования некоторых данных
    def test_plan_dialog(self):
        all_group_names = self._plan_model.get_column_values(1)
        all_group_names = list(dict.fromkeys(all_group_names))
        dialog = GroupEditDialog(all_group_names, field_label="Место проведения", title="Редактирование места проведения", parent=self)
        if dialog.exec():
            selected_groups, value = dialog.get_result()
            
        

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
                

    def test_adding_info(self):
        self._plan_model.updateCellsByCondition(1, "B", 4, "Gay\nnot\nnatural")
        self.ui.tableView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)        

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
        """
        for i, block in enumerate(blocks_maga, 1):
            print(f"\nБлок {i}:")
            print(f"Заголовок: {block['title']}")
            print("Данные:")
            block_df = pd.DataFrame(block['data'])
            print(block_df.to_string(index=False, header=False))"""


    # Функция для установки границ у ячейки
    def set_cell_border(self, cell, **kwargs):
        """
        Устанавливает границы ячейки.
        Параметры можно передавать как: top="single", bottom="single", left="single", right="single"
        """
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        tcBorders = OxmlElement('w:tcBorders')
        for edge in ('top', 'left', 'bottom', 'right'):
            edge_data = kwargs.get(edge)
            if edge_data:
                tag = f'w:{edge}'
                element = OxmlElement(tag)
                element.set(qn('w:val'), edge_data)         # тип линии
                element.set(qn('w:sz'), '4')                # толщина (1/8 pt)
                element.set(qn('w:space'), '0')             # отступ
                element.set(qn('w:color'), '000000')        # цвет (чёрный)
                tcBorders.append(element)
        tcPr.append(tcBorders)

    # Установка шрифта Times New Roman, размер 10 pt
    def set_cell_font(self, cell, font_name="Times New Roman", font_size=10):
        paragraph = cell.paragraphs[0]
        run = paragraph.runs[0] if paragraph.runs else paragraph.add_run()
        font = run.font
        font.name = font_name
        run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
        font.size = Pt(font_size)

    def fill_the_shablon_rows(self):
        doc = Document("E:/Python/Magistr_Project/Test_results/shablon_plan.docx")
        data = [
            ["ПМИ-101", "Иванов И.И.", "ООО Рога и Копыта"],
            ["ПМИ-102", "Петров П.П.", "ООО Пример"],
            ["ПМИ-102", "Петров П.П.", "ООО Пример"],
            ["ПМИ-102", "Петров П.П.", "ООО Пример"],
            ["ПМИ-101", "Иванов И.И.", "ООО Рога и Копыта"],
            ["ПМИ-102", "Петров П.П.", "ООО Пример"],
            ["ПМИ-102", "Петров П.П.", "ООО Пример"],
            ["ПМИ-102", "Петров П.П.", "ООО Пример"],
            ["ПМИ-101", "Иванов И.И.", "ООО Рога и Копыта"],
            ["ПМИ-102", "Петров П.П.", "ООО Пример"],
            ["ПМИ-102", "Петров П.П.", "ООО Пример"],
            ["ПМИ-102", "Петров П.П.", "ООО Пример"],
            ["ПМИ-101", "Иванов И.И.", "ООО Рога и Копыта"],
            ["ПМИ-102", "Петров П.П.", "ООО Пример"],
            ["ПМИ-102", "Петров П.П.", "ООО Пример"],
            ["ПМИ-102", "Петров П.П.", "ООО Пример"],
        ]
        table = doc.tables[0]
        start_row = 2
        self.fill_the_table_rows(table, data, start_row)
        print("Сохранение успешно")
        doc.save("Test_results/plan_zapolnen.docx")

    def fill_the_shablon(self):
        doc = Document("E:/Python/Magistr_Project/Test_results/shablon_plan.docx")

        # Предположим, что нужная таблица — первая в документе
        table = doc.tables[0]

        # Список номеров групп, которые нужно вставить
        nomera_grupp = ["4218", "4321", "4332"]
        other_data = ["gay","is", "sex", "real"]

        # Найдём индекс столбца с заголовком "№ группы"
        header_row = table.rows[0]
        column_index = None
        for i, cell in enumerate(header_row.cells):
            if cell.text.strip() == "№ гр.":
                column_index = i
                break

        # Проверка, что столбец найден
        #Заполнение таблицы мой вариант
        self.fill_the_table_col(table, column_index, nomera_grupp)
        self.fill_the_table_col(table, column_index + 1, other_data)
        doc.save("Результат_с_границами.docx")
        print("Файл сохранён с границами.")
        # Заполнение таблицы
        """
        if column_index is not None:
            for i, group in enumerate(nomera_grupp):
                row_index = i + 2  # начинаем с 3-й строки
                if row_index >= len(table.rows):
                    table.add_row()
                cell = table.rows[row_index].cells[column_index]
                cell.text = group
                self.set_cell_font(cell, font_name="Times New Roman", font_size=10)
                self.set_cell_border(cell, top="single", bottom="single", left="single", right="single")

            doc.save("Результат_с_границами.docx")
            print("Файл сохранён с границами.")
        else:
            print("Не найден столбец '№ группы'")"""

    # Заполнение строки word
    def fill_the_table_rows(self,table, data, start_row):
        for i, row_data in enumerate(data):
            # Если строки не хватает — добавляем
            row_index = start_row + i
            if start_row + i >= len(table.rows):
                table.add_row()

            for j, value in enumerate(row_data):
                cell = table.cell(row_index, j)
                cell.text = str(value)
                self.set_cell_font(cell, font_name="Times New Roman", font_size=10)
                self.set_cell_border(cell, top="single", bottom="single", left="single", right="single")

    # Заполнение столбца word
    def fill_the_table_col(self,table, column_index, data):
        for i, group in enumerate(data):
                row_index = i + 2  # начинаем с 3-й строки
                if row_index >= len(table.rows):
                    table.add_row()
                cell = table.rows[row_index].cells[column_index]
                cell.text = group
                self.set_cell_font(cell, font_name="Times New Roman", font_size=10)
                self.set_cell_border(cell, top="single", bottom="single", left="single", right="single")



    def upload_word(self, df):
        # Создаем документ Word
        doc = Document()
        doc.add_heading('Данные из Excel', level=1)

        # Добавляем таблицу (с заголовками)
        table = doc.add_table(rows=1, cols=len(df.columns))
        table.style = 'Table Grid'

        # Заголовки
        hdr_cells = table.rows[0].cells
        for i, column in enumerate(df.columns):
            hdr_cells[i].text = str(column)

        # Данные
        for _, row in df.iterrows():
            row_cells = table.add_row().cells
            for i, cell in enumerate(row):
                row_cells[i].text = str(cell)

        # Сохраняем документ
        doc.save("Результат.docx")


    def load_table(self):
        fname, _ = QFileDialog.getOpenFileName(
            self, "Choose file", "", "Excel Files (*.xlsx *.xls *.xlsm)")
        if not fname:
            return
        excel_file = pd.ExcelFile(fname)
        #sheet_names = excel_file.sheet_names
        #sheet_data = {name: pd.read_excel(excel_file, sheet_name=name) for name in sheet_names}
        sheet_names = excel_file.sheet_names
        print("Листы в файле:")
        for name in sheet_names:
            print(f" - {name}")

        # Читаем данные с каждого листа и выводим первые 3 строки
        sheet_data = {}
        for name in sheet_names:
            df = pd.read_excel(excel_file, sheet_name=name)
            sheet_data[name] = df
            print(f"\nПервые строки с листа: {name}")
            print(df.head(3))
        #bakalavriat = pd.read_excel(fname, 0)
        #magistratura = pd.read_excel(fname, 1)
        print(sheet_data)

    """
    # функции для фильтрации tableView
    def apply_filter(self):
        text = self.ui.searchPlanLineEdit.text()
        column = self.ui.planSearchComboBox.currentData()
        self.proxy_model.setFilterKeyColumn(column)
        self.proxy_model.setFilterFixedString(text)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    """

    def test_function(self):
        print('test')

    def cabinet_function(self):
        print('cabinet button')

    def faq_function(self):
        print('faq button')

    def genOtch_function(self):
        print('genOtch button')

    def genPlan_function(self):
        print('genOtch button')

    def exit_function(self):
        sys.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())