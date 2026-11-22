import os
import platform
import sqlite3
import subprocess

from PySide6.QtWidgets import QMessageBox

import Models.dbhandler as dbh
from Models.model import PlanTableModel
from View.prepod_dialog import PrepodDialog
from View.startosta_dialog import StarostaDialog
from window_support import (
    locate_saved_file,
    prepare_table,
    release_saved_copy,
    split_expired_documents,
)


def _yes_no(value, _row):
    return "Да" if value else "Нет"


def _file_name(value, _row):
    text = "" if value is None else str(value)
    name = os.path.basename(text)
    return name or text


def _full_path(value, _row):
    return "" if value is None else str(value)


class DatabasePage:
    def _mark_db_tab(self, active):
        idle = "QPushButton { color: white; text-align: center; }"
        marked = (
            "QPushButton { color: white; text-align: center;"
            " background-color: rgba(255, 255, 255, 48);"
            " border: 1px solid rgba(255, 255, 255, 90); }"
        )
        buttons = {
            "docs": self.ui.dbPlansPushButton,
            "teachers": self.ui.dbPrepodsPushButton,
            "starostas": self.ui.dbStarostaPushButton,
        }
        for name, button in buttons.items():
            button.setStyleSheet(marked if name == active else idle)

    def selected_db_row(self):
        indexes = self.ui.dataBaseTableView.selectedIndexes()
        if self._db_model is None or not indexes:
            QMessageBox.warning(self, "Ошибка", "Выберите строку в таблице")
            return None
        return self._db_model.get_row(indexes[0].row())

    def _document_from_db(self):
        data = self.selected_db_row()
        if data is None:
            return None
        rows = dbh.select_document_by_id(data[0])
        if not rows:
            QMessageBox.warning(self, "Ошибка", "Документ не найден")
            return None
        return rows[0]

    def open_document(self):
        row = self._document_from_db()
        if row is None:
            return
        file_path = locate_saved_file(row[-1])
        if file_path is None:
            QMessageBox.warning(self, "Ошибка", "Файл лежит вне папки сохранений")
            return
        system = platform.system()
        target = os.fspath(file_path)
        try:
            if system == "Windows":
                os.startfile(target)
            elif system == "Darwin":
                subprocess.run(["open", target], check=True)
            else:
                subprocess.run(["xdg-open", target], check=True)
        except (OSError, subprocess.CalledProcessError) as exc:
            QMessageBox.warning(self, "Ошибка", f"Не удалось открыть файл: {exc}")

    def defend_doucment(self):
        row = self._document_from_db()
        if row is None:
            return
        new_status = 1 if row[5] == 0 else 0
        try:
            dbh.defend_document(row[0], new_status)
        except sqlite3.Error as exc:
            QMessageBox.warning(self, "Ошибка", f"Не удалось изменить защиту: {exc}")
            return
        self.upload_db_docs()

    def _confirm_drop_row_only(self):
        answer = QMessageBox.question(
            self,
            "Удалить только запись из базы?",
            "Удалить только запись из базы?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        return answer == QMessageBox.Yes

    def _remove_document_record(self, row):
        # сначала файл в Saves, строку снимаю только если файл ушёл или его уже не было
        status, detail = release_saved_copy(row[-1])
        if status == "outside":
            if not self._confirm_drop_row_only():
                return False
        elif status == "kept":
            QMessageBox.warning(
                self,
                "Ошибка",
                f"Файл не удалён, запись в базе сохранена: {detail}",
            )
            return False
        try:
            dbh.remove_document(row[0])
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Защита", "Документ защищён и не может быть удалён")
            return False
        except sqlite3.Error as exc:
            QMessageBox.warning(self, "Ошибка", f"Не удалось удалить запись: {exc}")
            return False
        return True

    def remove_document(self):
        row = self._document_from_db()
        if row is None:
            return
        if row[5] == 1:
            QMessageBox.warning(self, "Защита", "Документ защищён и не может быть удалён")
            return
        if self._remove_document_record(row):
            self.upload_db_docs()

    def upload_db_starosta(self):
        self.ui.dbPageStackedWidget.setCurrentIndex(1)
        try:
            data = dbh.load_starostas()
        except sqlite3.Error as exc:
            QMessageBox.warning(self, "Ошибка", str(exc))
            return
        try:
            teachers = dbh.load_teachers()
        except sqlite3.Error as exc:
            QMessageBox.warning(self, "Ошибка", str(exc))
            return
        names = {
            row[0]: " ".join(part for part in (row[1], row[2], row[3]) if part) for row in teachers
        }

        def curator(value, _row):
            if value in names:
                return names[value]
            return "" if value is None else str(value)

        headers = ["id", "Куратор", "Фамилия", "Имя", "Отчество", "Группа", "Почта", "Телефон"]
        self._db_model = PlanTableModel(data, headers, editable=False, display={1: curator})
        self.ui.dataBaseTableView.setModel(self._db_model)
        prepare_table(self.ui.dataBaseTableView, hide=(0,), contents=(1,))
        self._mark_db_tab("starostas")

    def add_db_starosta(self):
        try:
            teachers = dbh.load_teachers()
        except sqlite3.Error as exc:
            QMessageBox.warning(self, "Ошибка", f"Не удалось открыть список преподавателей: {exc}")
            return
        dialog = StarostaDialog(teachers=teachers, parent=self)
        if not dialog.exec():
            return
        try:
            dbh.insert_starosta(*dialog.get_data())
        except (sqlite3.Error, TypeError, ValueError) as exc:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить старосту: {exc}")
            return
        self.upload_db_starosta()

    def edit_db_starosta(self):
        try:
            teachers = dbh.load_teachers()
        except sqlite3.Error as exc:
            QMessageBox.warning(self, "Ошибка", f"Не удалось открыть список преподавателей: {exc}")
            return
        row = self.selected_db_row()
        if row is None:
            return
        dialog = StarostaDialog(teachers=teachers, starosta_data=list(row[1:]), parent=self)
        if not dialog.exec():
            return
        try:
            dbh.update_starosta(row[0], dialog.get_data())
        except (sqlite3.Error, TypeError, ValueError) as exc:
            QMessageBox.warning(self, "Ошибка", f"Не удалось изменить старосту: {exc}")
            return
        self.upload_db_starosta()

    def remove_db_starosta(self):
        row = self.selected_db_row()
        if row is None:
            return
        try:
            dbh.remove_starosta(row[0])
        except sqlite3.Error as exc:
            QMessageBox.warning(self, "Ошибка", f"Не удалось удалить старосту: {exc}")
            return
        self.upload_db_starosta()

    def upload_db_teachers(self):
        self.ui.dbPageStackedWidget.setCurrentIndex(0)
        try:
            data = dbh.load_teachers()
        except sqlite3.Error as exc:
            QMessageBox.warning(self, "Ошибка", str(exc))
            return
        headers = ["id", "Фамилия", "Имя", "Отчество", "Степень", "Должность", "Почта", "Телефон"]
        self._db_model = PlanTableModel(data, headers, editable=False)
        self.ui.dataBaseTableView.setModel(self._db_model)
        prepare_table(self.ui.dataBaseTableView, hide=(0,))
        self._mark_db_tab("teachers")

    def add_db_prepod(self):
        dialog = PrepodDialog(parent=self)
        if not dialog.exec():
            return
        try:
            dbh.insert_teacher(*dialog.get_data())
        except (sqlite3.Error, TypeError, ValueError) as exc:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить преподавателя: {exc}")
            return
        self.upload_db_teachers()

    def edit_db_prepod(self):
        row = self.selected_db_row()
        if row is None:
            return
        dialog = PrepodDialog(data=row[1:], parent=self)
        if not dialog.exec():
            return
        try:
            dbh.update_teacher(row[0], dialog.get_data())
        except (sqlite3.Error, TypeError, ValueError) as exc:
            QMessageBox.warning(self, "Ошибка", f"Не удалось изменить преподавателя: {exc}")
            return
        self.upload_db_teachers()

    def remove_db_prepod(self):
        row = self.selected_db_row()
        if row is None:
            return
        try:
            dbh.remove_teacher(row[0])
        except sqlite3.Error as exc:
            QMessageBox.warning(self, "Ошибка", f"Не удалось удалить преподавателя: {exc}")
            return
        self.upload_db_teachers()

    def upload_db_docs(self, review_retention=False):
        self.ui.dbPageStackedWidget.setCurrentIndex(2)
        try:
            data = dbh.load_docs()
        except sqlite3.Error as exc:
            QMessageBox.warning(self, "Ошибка", str(exc))
            return
        headers = ["id", "Год", "Тип", "Дата создания", "Создатель", "Защищено", "Файл"]
        self._db_model = PlanTableModel(
            data,
            headers,
            editable=False,
            display={5: _yes_no, 6: _file_name},
            tooltips={6: _full_path},
        )
        self.ui.dataBaseTableView.setModel(self._db_model)
        prepare_table(self.ui.dataBaseTableView, hide=(0,), contents=(6,))
        self._mark_db_tab("docs")
        if review_retention:
            self.review_document_retention(data)

    def review_document_retention(self, rows):
        expired, protected = split_expired_documents(rows)
        if not expired and not protected:
            return
        self._retention_reviewed = True
        lines = []
        if expired:
            lines.append("Незащищённые документы сроком 5 лет и больше:")
            lines.extend(self._document_line(row) for row in expired)
        if protected:
            lines.append("Защищённые документы сроком 5 лет и больше не удаляются:")
            lines.extend(self._document_line(row) for row in protected)
        if not expired:
            QMessageBox.information(self, "Срок хранения", "\n".join(lines))
            return
        answer = QMessageBox.question(
            self,
            "Срок хранения",
            "\n".join(lines) + "\n\nУдалить незащищённые документы?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if answer != QMessageBox.Yes:
            return
        for row in expired:
            self._remove_document_record(row)
        self.upload_db_docs()

    def _document_line(self, row):
        created = row[3] if len(row) > 3 else ""
        doc_type = row[2] if len(row) > 2 else ""
        return f"— {doc_type}, {created}"
