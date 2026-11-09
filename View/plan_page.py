import pandas as pd
from docx import Document
from PySide6.QtWidgets import QFileDialog, QMessageBox

import Models.datahandler as dh
from Models.docx_writer import fill_the_table_rows
from View.planaddingdialogs import GroupEditDialog
from window_support import log_exception, save_registered_copy, shablon_plan_path


def plan_replace_needs_confirm(row_count, replaces_rows):
    """Истина, когда загрузка сотрёт уже заполненную таблицу."""
    return row_count > 0 and bool(replaces_rows)


class PlanPage:
    def save_plan_as(self):
        options = QFileDialog.Options()
        fname, _ = QFileDialog.getSaveFileName(
            self, "Сохранить файл", "", "Word файлы (*.docx)", options=options
        )
        if not fname:
            return
        try:
            doc = Document(shablon_plan_path)
            data_for_save = self._plan_model.get_data_without_id()
            table = doc.tables[0]
            start_row = 2
            fill_the_table_rows(table, data_for_save, start_row)
            doc.save(fname)
        except Exception as exc:
            log_exception()
            QMessageBox.warning(self, "Ошибка", str(exc))

    def save_plan_new(self):
        try:
            doc = Document(shablon_plan_path)
            data_for_save = self._plan_model.get_data_without_id()
            table = doc.tables[0]
            fill_the_table_rows(table, data_for_save, 2)
            save_registered_copy(self, doc, "План")
        except Exception as exc:
            log_exception()
            QMessageBox.warning(self, "Ошибка", str(exc))

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
                key = dh.normalize_group(group)
                self._plan_model.updateCellsByCondition(
                    1,
                    lambda cell, key=key: dh.normalize_group(cell) == key,
                    col,
                    str(value),
                )

    def _merge_student_blocks(self, additional_data):
        groups = self._plan_model.get_col(1)
        practices = self._plan_model.get_col(2)
        updated = []
        for group, practice in zip(groups, practices):
            block = dh.choose_student_block(additional_data, group, practice)
            if block is None:
                updated.append(practice)
            else:
                updated.append(dh.apply_student_block(practice, block))
        self._plan_model.set_col(2, updated)

    def _ask_replace_plan(self):
        answer = QMessageBox.question(
            self,
            "Заменить текущий план?",
            "Заменить текущий план?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        return answer == QMessageBox.Yes

    def load_nagruzka(self):
        if plan_replace_needs_confirm(self._plan_model.rowCount(), not self._table_loaded):
            if not self._ask_replace_plan():
                return
        fname, _ = QFileDialog.getOpenFileName(
            self, "Choose file", "", "Excel Files (*.xlsx *.xls *.xlsm)"
        )
        if not fname:
            return
        try:
            data = pd.read_excel(fname, header=None)
            if self._table_loaded:
                additional_data = dh.extract_additional_info_form_nagruzka(data)
            else:
                extracted_data = dh.extract_data(data)
        except (OSError, ValueError, IndexError, KeyError) as exc:
            log_exception()
            QMessageBox.warning(self, "Ошибка", str(exc))
            return
        except Exception as exc:
            log_exception()
            QMessageBox.warning(self, "Ошибка", str(exc))
            return
        if self._table_loaded:
            self._merge_student_blocks(additional_data)
        else:
            self._plan_model.clear()
            if extracted_data:
                self._plan_model.insertRows(0, len(extracted_data), extracted_data)
        self._nagruzka_loaded = True
        self.ui.tableView.resizeRowsToContents()

    def load_table_new(self):
        if plan_replace_needs_confirm(self._plan_model.rowCount(), True):
            if not self._ask_replace_plan():
                return
        fname, _ = QFileDialog.getOpenFileName(
            self, "Choose file", "", "Excel Files (*.xlsx *.xls *.xlsm)"
        )
        if not fname:
            return
        try:
            with pd.ExcelFile(fname) as book:
                if len(book.sheet_names) < 2:
                    raise ValueError("В файле плана нужны два листа")
                baka = pd.read_excel(book, 0, header=None)
                maga = pd.read_excel(book, 1, header=None)
            # keywords = ["практика", "магистратура"]

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

            # print(blocks_maga)
            blocks_baka_tr = dh.transform_practice_data(blocks)
            blocks_maga_tr = dh.transform_practice_data(blocks_maga, len(blocks_baka_tr))
            combined_blocks = blocks_baka_tr + blocks_maga_tr
        except (OSError, ValueError, IndexError, KeyError) as exc:
            log_exception()
            QMessageBox.warning(self, "Ошибка", str(exc))
            return
        except Exception as exc:
            log_exception()
            QMessageBox.warning(self, "Ошибка", str(exc))
            return
        self._plan_model.clear()
        if combined_blocks:
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
