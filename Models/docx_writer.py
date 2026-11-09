from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt


def set_cell_border(cell, **kwargs):
    """
    Устанавливает границы ячейки.
    Параметры можно передавать как: top="single", bottom="single", left="single", right="single"
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = f"w:{edge}"
            element = OxmlElement(tag)
            element.set(qn("w:val"), edge_data)  # тип линии
            element.set(qn("w:sz"), "4")  # толщина (1/8 pt)
            element.set(qn("w:space"), "0")  # отступ
            element.set(qn("w:color"), "000000")  # цвет (чёрный)
            tcBorders.append(element)
    tcPr.append(tcBorders)


def set_cell_font(cell, font_name="Times New Roman", font_size=10):
    paragraph = cell.paragraphs[0]
    run = paragraph.runs[0] if paragraph.runs else paragraph.add_run()
    font = run.font
    font.name = font_name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), font_name)
    font.size = Pt(font_size)


def fill_the_table_rows(table, data, start_row):
    for i, row_data in enumerate(data):
        # Если строки не хватает — добавляем
        row_index = start_row + i
        if start_row + i >= len(table.rows):
            table.add_row()

        for j, value in enumerate(row_data):
            cell = table.cell(row_index, j)
            cell.text = str(value)
            set_cell_font(cell, font_name="Times New Roman", font_size=10)
            set_cell_border(cell, top="single", bottom="single", left="single", right="single")


def fill_the_table_col(table, column_index, data):
    for i, group in enumerate(data):
        row_index = i + 2  # начинаем с 3-й строки
        if row_index >= len(table.rows):
            table.add_row()
        cell = table.rows[row_index].cells[column_index]
        cell.text = group
        set_cell_font(cell, font_name="Times New Roman", font_size=10)
        set_cell_border(cell, top="single", bottom="single", left="single", right="single")
