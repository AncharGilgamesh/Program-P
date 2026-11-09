import datetime
import os
import sqlite3
import traceback
from pathlib import Path

from PySide6.QtWidgets import QMessageBox

import Models.dbhandler as dbh

base_dir = os.path.dirname(os.path.abspath(__file__))
help_path = os.path.join(base_dir, "", "help.html")
shablon_plan_path = os.path.join(base_dir, "Shablons", "shablon_plan.docx")
shablon_otch_path = os.path.join(base_dir, "Shablons", "shablon_otchet.docx")
# Строки шаблона отчёта, с которых пишутся данные: у первой таблицы одна строка
# шапки, у пятой — четыре. Остальные таблицы начинаются после двух строк шапки.
OTCHET_TABLE_START_ROWS = (1, 2, 2, 2, 4, 2)
RETENTION_YEARS = 5


def locate_saved_file(stored, root=None):
    """Путь внутри текущего Saves или None.

    Относительный путь считается от корня проекта. Абсолютный путь из другой
    копии папки находится по имени файла, если оно уже лежит в текущем Saves.
    """
    text = "" if stored is None else str(stored).strip()
    if not text:
        return None
    base = Path(root or base_dir).resolve()
    saves = (base / "Saves").resolve()
    candidate = Path(text)
    absolute = candidate.is_absolute()
    if not absolute:
        candidate = base / candidate
    try:
        resolved = candidate.resolve()
    except OSError:
        return None
    try:
        resolved.relative_to(saves)
    except ValueError:
        if not absolute:
            return None
        moved = saves / Path(text).name
        if moved.is_file():
            return moved.resolve()
        return None
    return resolved


def path_inside_saves(file_path, root=None):
    """Истина, если путь после resolve лежит внутри каталога Saves."""
    text = "" if file_path is None else str(file_path).strip()
    if not text:
        return False
    base = Path(root or base_dir).resolve()
    saves = (base / "Saves").resolve()
    candidate = Path(text)
    if not candidate.is_absolute():
        candidate = base / candidate
    try:
        resolved = candidate.resolve()
    except OSError:
        return False
    try:
        resolved.relative_to(saves)
    except ValueError:
        return False
    return True


def years_before(day, years):
    try:
        return day.replace(year=day.year - years)
    except ValueError:
        return day.replace(year=day.year - years, day=28)


def parse_created_date(value):
    text = str(value or "").strip()
    for fmt in ("%Y.%m.%d", "%Y-%m.%d", "%d.%m.%Y"):
        try:
            return datetime.datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def split_expired_documents(rows, today=None):
    """Делит документы старше срока хранения на незащищённые и защищённые."""
    today = today or datetime.date.today()
    limit = years_before(today, RETENTION_YEARS)
    expired = []
    protected = []
    for row in rows:
        created = parse_created_date(row[3] if len(row) > 3 else None)
        if created is None or created > limit:
            continue
        if len(row) > 5 and row[5] == 1:
            protected.append(row)
        else:
            expired.append(row)
    return expired, protected


def saves_filename(year, doc_type, moment=None):
    """Год, тип и дата-время, чтобы два сохранения за день не затирали один файл."""
    moment = moment or datetime.datetime.now()
    marker = "p" if doc_type == "План" else "o"
    stamp = moment.strftime("%Y%m%d_%H%M%S_%f")
    return f"{year}_{marker}_{stamp}.docx"


def log_exception():
    """Дописывает время и трассу текущего исключения. Пароли и поля ввода не пишет."""
    try:
        folder = os.path.join(base_dir, "logs")
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, "app.log")
        moment = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(f"{moment}\n{traceback.format_exc()}\n")
    except OSError:
        return


def save_registered_copy(window, doc, doc_type):
    year = datetime.datetime.now().year
    filename = saves_filename(year, doc_type)
    saves_dir = os.path.join(base_dir, "Saves")
    os.makedirs(saves_dir, exist_ok=True)
    save_path = os.path.join(saves_dir, filename)
    try:
        doc.save(save_path)
    except OSError as exc:
        log_exception()
        QMessageBox.warning(window, "Ошибка", f"Не удалось сохранить файл: {exc}")
        return
    created = datetime.datetime.now().strftime("%Y.%m.%d")
    try:
        dbh.insert_document(year, doc_type, created, window.user, f"Saves/{filename}", 0)
    except sqlite3.Error as exc:
        log_exception()
        QMessageBox.warning(
            window,
            "Ошибка",
            f"Файл сохранён, но записать его в базу не удалось: {exc}",
        )


def remembered_username_path(directory=None):
    """Логин «запомнить меня» лежит у пользователя, не в общей базе."""
    folder = directory or os.path.join(os.path.expanduser("~"), ".magistr_project")
    return os.path.join(folder, "remembered_username")


def save_remembered_username(username, directory=None):
    path = remembered_username_path(directory)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(str(username).strip())


def read_remembered_username(directory=None):
    path = remembered_username_path(directory)
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as handle:
        text = handle.read().strip()
    return text or None


def clear_remembered_username(directory=None):
    path = remembered_username_path(directory)
    if os.path.isfile(path):
        os.remove(path)
