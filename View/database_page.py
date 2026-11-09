import os
import platform
import sqlite3
import subprocess

from PySide6.QtWidgets import QMessageBox

import Models.dbhandler as dbh
from Models.model import PlanTableModel
from View.prepod_dialog import PrepodDialog
from View.startosta_dialog import StarostaDialog
from window_support import path_inside_saves, split_expired_documents


class DatabasePage:
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
        file_path = row[-1]
        if not path_inside_saves(file_path):
            QMessageBox.warning(self, "Ошибка", "Файл лежит вне папки сохранений")
            return
        system = platform.system()
        try:
            if system == "Windows":
                os.startfile(file_path)
            elif system == "Darwin":
                subprocess.run(["open", file_path], check=True)
            else:
                subprocess.run(["xdg-open", file_path], check=True)
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

    def remove_document(self):
        row = self._document_from_db()
        if row is None:
            return
        if row[5] == 1:
            QMessageBox.warning(self, "Защита", "Документ защищён и не может быть удалён")
            return
        file_path = row[-1]
        if not path_inside_saves(file_path):
            QMessageBox.warning(self, "Ошибка", "Файл лежит вне папки сохранений")
            return
        try:
            dbh.remove_document(row[0])
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Защита", "Документ защищён и не может быть удалён")
            return
        except sqlite3.Error as exc:
            QMessageBox.warning(self, "Ошибка", f"Не удалось удалить запись: {exc}")
            return
        try:
            if file_path:
                os.remove(file_path)
        except OSError as exc:
            QMessageBox.warning(self, "Ошибка", f"Запись удалена, но файл не удалён: {exc}")
        self.upload_db_docs()

    def upload_db_starosta(self):
        self.ui.dbPageStackedWidget.setCurrentIndex(1)
        data = dbh.load_starostas()
        headers = ["id", "id_Куратора", "Фамилия", "Имя", "Отчество", "Группа", "Почта", "Номер"]
        self._db_model = PlanTableModel(data, headers, editable=False)
        self.ui.dataBaseTableView.setModel(self._db_model)

    def add_db_starosta(self):
        teachers = dbh.load_teachers()
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
        teachers = dbh.load_teachers()
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
        data = dbh.load_teachers()
        headers = ["id", "Фамилия", "Имя", "Отчество", "Степень", "Должность", "Почта", "Номер"]
        self._db_model = PlanTableModel(data, headers, editable=False)
        self.ui.dataBaseTableView.setModel(self._db_model)

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
        data = dbh.load_docs()
        headers = ["id", "Год", "Тип", "Дата создания", "Создатель", "Защищено", "Путь"]
        self._db_model = PlanTableModel(data, headers, editable=False)
        self.ui.dataBaseTableView.setModel(self._db_model)
        if review_retention:
            self.review_document_retention(data)

    def review_document_retention(self, rows):
        expired, protected = split_expired_documents(rows)
        if not expired and not protected:
            return
        self._retention_reviewed = True
        lines = []
        if expired:
            lines.append("Незащищённые документы старше 5 лет:")
            lines.extend(self._document_line(row) for row in expired)
        if protected:
            lines.append("Защищённые документы старше 5 лет не удаляются:")
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
            if not path_inside_saves(row[-1]):
                QMessageBox.warning(self, "Ошибка", "Файл лежит вне папки сохранений")
                continue
            try:
                dbh.remove_document(row[0])
            except sqlite3.Error as exc:
                QMessageBox.warning(self, "Ошибка", f"Не удалось удалить запись: {exc}")
                continue
            try:
                if row[-1]:
                    os.remove(row[-1])
            except OSError as exc:
                QMessageBox.warning(self, "Ошибка", f"Запись удалена, но файл не удалён: {exc}")
        self.upload_db_docs()

    def _document_line(self, row):
        created = row[3] if len(row) > 3 else ""
        doc_type = row[2] if len(row) > 2 else ""
        return f"— {doc_type}, {created}"
