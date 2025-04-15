import sys

import pandas as pd
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog

from View.workspace import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.dataToolButton.clicked.connect(self.test_function)
        self.ui.cabinetToolButton.clicked.connect(self.cabinet_function)
        self.ui.exitToolButton.clicked.connect(self.exit_function)
        self.ui.loadTableButton.clicked.connect(self.load_table_new)
        self.ui.loadNagruzkaButton.clicked.connect(self.fill_the_shablon)

    def load_table_new(self):
        fname, _ = QFileDialog.getOpenFileName(
            self, "Choose file", "", "Excel Files (*.xlsx *.xls *.xlsm)")
        if not fname:
            return
        bakalavriat = pd.read_excel(fname, 0)
        magistratura = pd.read_excel(fname, 1)
        self.upload_word(bakalavriat)


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

    def fill_the_shablon(self):
        doc = Document("E:/Python/Magistr_Project/shablon_plan.docx")

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
        self.fill_the_table(table, column_index, nomera_grupp)
        self.fill_the_table(table, column_index + 1, other_data)
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

    def fill_the_table(self,table, column_index, data):
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