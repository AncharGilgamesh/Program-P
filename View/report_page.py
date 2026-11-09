from docx import Document
from PySide6.QtWidgets import QFileDialog, QInputDialog, QMessageBox

import Models.datahandler as dh
from Models.docx_writer import fill_the_table_rows
from Models.model import PlanTableModel, ResultTableModel
from View.meetingdatedialog import MeetingDateDialog
from window_support import (
    OTCHET_TABLE_START_ROWS,
    log_exception,
    save_registered_copy,
    shablon_otch_path,
)


def show_fio_dialog(parent=None):
    text, ok = QInputDialog.getText(parent, "Введите ФИО", "Фамилия и инициалы:")
    if ok and text.strip():
        return text.strip()
    return None


class ReportPage:
    def _otchet_models(self):
        return (
            self._oth_frst_stg_model,
            self._oth_scnd_std_model,
            self._oth_thrd_stg_model,
            self._fourth_stg_model,
            self._fiveth_stg_model,
            self._sixth_stg_model,
        )

    def build_otchet_document(self):
        doc = Document(shablon_otch_path)
        for table, model, start_row in zip(
            doc.tables, self._otchet_models(), OTCHET_TABLE_START_ROWS
        ):
            fill_the_table_rows(table, model.get_data(), start_row)
        return doc

    def save_otchet_as(self):
        options = QFileDialog.Options()
        fname, _ = QFileDialog.getSaveFileName(
            self, "Сохранить файл", "", "Word файлы (*.docx)", options=options
        )
        if not fname:
            return
        try:
            doc = self.build_otchet_document()
            doc.save(fname)
        except Exception as exc:
            log_exception()
            QMessageBox.warning(self, "Ошибка", str(exc))

    def save_otchet(self):
        try:
            doc = self.build_otchet_document()
            save_registered_copy(self, doc, "Отчет")
        except Exception as exc:
            log_exception()
            QMessageBox.warning(self, "Ошибка", str(exc))

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
            self._oth_thrd_stg_model.set_col(
                target_column, [fio] * self._oth_thrd_stg_model.rowCount()
            )  # Вставить ФИО во все строки

    def otch_make_all_came(self):
        values = self._oth_scnd_std_model.get_col(3)
        self._oth_scnd_std_model.set_col(4, values)

    def set_otchet_resizing(self):
        self.ui.otchFirstTableView.resizeRowsToContents()
        self.ui.otchSecondTableView.resizeRowsToContents()
        self.ui.otchThirdTableView.resizeRowsToContents()
        self.ui.otchFourthTableView.resizeRowsToContents()

        # self.ui.otchFivethTableView.resizeRowsToContents()
        self.ui.otchFivethTableView.verticalHeader().setDefaultSectionSize(40)
        self.ui.otchSixthTableView.resizeRowsToContents()

    def add_meting_date(self):
        data_for_meeting = self._oth_frst_stg_model.get_data()
        data_fin = dh.get_group_practice_keys_frst_stg(data_for_meeting)
        dialog = MeetingDateDialog(data_fin, parent=self)

        if dialog.exec():
            selected_keys, date_str = dialog.get_results()
            rows_to_update = dh.get_target_row_indices(data_for_meeting, selected_keys)
            # можно выделить это в отдельную функцию для добавления по индексам!!!!!!!!!
            for row in rows_to_update:
                # столбец 5 — это "Дата проведения собрания"
                self._oth_frst_stg_model.setData(self._oth_frst_stg_model.index(row, 5), date_str)

    def load_plan(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Choose file", "", "Word файлы (*.docx)")
        if not fname:
            return
        try:
            data = dh.read_plan_from_docx(fname)
            table1 = dh.parse_practice_table(data[1:])  # пропускаем заголовки
            table2 = dh.parse_second_table(data[1:])
            table3 = dh.parse_third_table(data[1:])
            table4 = dh.parse_fourth_table(table2)
            table5, skipped_groups = dh.parse_fiveth_table(table2)
            table6 = dh.parse_sixth_table(data[1:])
            loaded = (
                (self._oth_frst_stg_model, table1),
                (self._oth_scnd_std_model, table2),
                (self._oth_thrd_stg_model, table3),
                (self._fourth_stg_model, table4),
                (self._fiveth_stg_model, table5),
                (self._sixth_stg_model, table6),
            )
        except Exception as exc:
            log_exception()
            QMessageBox.warning(self, "Ошибка", str(exc))
            return
        for model, rows in loaded:
            model.clear()
            if rows:
                model.insertRows(0, len(rows), rows)
        self.set_otchet_resizing()
        if skipped_groups:
            QMessageBox.warning(
                self,
                "Предупреждение",
                f"Пропущено строк без номера группы 4xxx: {skipped_groups}.",
            )

        # self._fourth_stg_model.insertRows(0, len(table4), table4)
        # вот тут представлены варианты изменения размера, нужно это все рассмотреть получше
        # self.ui.otchThirdTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.ui.otchThirdTableView.resizeRowsToContents()
        # Для четвертой таблицы попробуй взять инфу из второй таблицы и надо подредактировать
        # Сделать диалоговое окно, чтобы можно было заполнять таблицу из второй таблицы

    def to_next_stage(self):
        index = self.ui.stackedWidget.currentIndex() + 1
        if index == 6:
            return
        self.ui.otch_lbl_stage.setText(f"{index + 1} этап")
        self.ui.stackedWidget.setCurrentIndex(index)

    def to_prev_stage(self):
        index = self.ui.stackedWidget.currentIndex() - 1
        if index == -1:
            return
        self.ui.otch_lbl_stage.setText(f"{index + 1} этап")
        self.ui.stackedWidget.setCurrentIndex(index)

    def load_saved_otchet(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Choose file", "", "Word файлы (*.docx)")
        if not fname:
            return
        try:
            tables = dh.rows_from_saved_report(
                Document(fname), OTCHET_TABLE_START_ROWS, (6, 7, 3, 8, 8, 8)
            )
        except Exception as exc:
            log_exception()
            QMessageBox.warning(self, "Ошибка", str(exc))
            return
        models = self._otchet_models()
        if any(model.rowCount() > 0 for model in models):
            answer = QMessageBox.question(
                self,
                "Заменить текущий отчёт?",
                "Заменить текущий отчёт?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if answer != QMessageBox.Yes:
                return
        for model, rows in zip(models, tables):
            model.clear()
            if rows:
                model.insertRows(0, len(rows), rows)
        self.set_otchet_resizing()

    def set_otchet_tables_models(self):
        headers_for_first_stage = [
            "№",
            "Группа",
            "Направление\n/Специальность",
            "Семестр",
            "Вид практики",
            "Дата\nпроведения\nсобрания",
        ]
        headers_for_second_stage = [
            "№\nп/п",
            "Город",
            "Место проведения",
            "Направлено",
            "Прибыло",
            "Инструктаж по ТБ",
            "Факт. конец",
        ]
        headers_for_third_stage = ["Место", "Рук. от КАИ", "Рук. от предприятия"]
        headers_fourth_stage = [
            "Место\nпроведения\nпрактики",
            "В цехах",
            "Офис",
            "Инженерно-\nтехнические\nдолжности",
            "Научные\nлаборатории",
            "Студ.\n отряды",
            "Другое",
            "Оформление\nТБ на рабочем\nместе(да\нет)",
        ]
        headers_fiveth_stage = [
            "Группа",
            "Всего\nчел.",
            "Отл.",
            "Хор.",
            "Удовл.",
            "Неуд.",
            "Не\nзащитило",
            "Место\nзащиты",
        ]
        headers_sixth_stage = [
            "№",
            "Руководитель",
            "Должность",
            "Группа",
            "Вид\nпрактики",
            "Удовл.",
            "Хор.",
            "Отл.",
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
