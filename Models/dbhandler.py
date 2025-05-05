import os
import sqlite3
from PySide6.QtCore import QDate

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'DB', 'maindatabase.db')

def create_tables():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    create_docs_table()
    create_teachers_table()
    create_starosta_table()

def create_starosta_table():
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        query = ("""
            CREATE TABLE IF NOT EXISTS startostas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                teacher_id INTEGER,
                last_name VARCHAR(50) NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                middle_name VARCHAR(50),
                group_num VARCHAR(4),
                email VARCHAR(100) UNIQUE,
                phone VARCHAR(20)
            );
        """)
        cur.execute(query)
        con.commit()

def create_teachers_table():
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        query = ("""
            CREATE TABLE IF NOT EXISTS teachers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                last_name VARCHAR(50) NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                middle_name VARCHAR(50),
                academic_degree VARCHAR(50),
                academic_title VARCHAR(50),
                email VARCHAR(100) UNIQUE,
                phone VARCHAR(20)
                 );
        """)
        cur.execute(query)
        con.commit()

def create_docs_table():
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        query = ("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER,
                type TEXT,
                created TEXT,         -- 'YYYY-MM-DD'
                creator TEXT,
                protected INTEGER,    -- 0 или 1
                file_path TEXT
            );
            """)
        cur.execute(query)
        con.commit()


def update_teacher(id, data):
    """func."""
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        query = ("""
        UPDATE teachers
        SET last_name = ?,
            first_name = ?,
            middle_name = ?,
            academic_degree = ?,
            academic_title = ?,
            email = ?,
            phone = ?
        WHERE id = {}
        """.format(id))
        cur.execute(query, data)
        con.commit()

def insert_teacher(l_name, f_name, m_name, a_degree, a_title, email, phone):
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        query = """
            INSERT INTO teachers (last_name, first_name, middle_name, academic_degree, academic_title, email, phone)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        cur.execute(query, (
            l_name,
            f_name,
            m_name,
            a_degree,
            a_title,
            email,
            phone
        ))
        con.commit()


def insert_starosta(teacher_id, l_name, f_name, m_name, group, email, phone):
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        query = """
                INSERT INTO startostas (teacher_id, last_name, first_name, middle_name, group_num, email, phone)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            """
        cur.execute(query, (
                teacher_id,
                l_name,
                f_name,
                m_name,
                group,
                email,
                phone
            ))
        con.commit()


def insert_document(year: int, doc_type: str, created: str, creator: str, file_path: str, protected: bool = False):
    """
    Добавляет документ в таблицу `documents`.

    :param year: Год документа (например, 2024)
    :param doc_type: Тип ("План" или "Отчет")
    :param created: Дата создания в формате "YYYY-MM-DD"
    :param creator: Имя создателя документа
    :param file_path: Путь к файлу
    :param protected: Защищено ли от удаления (True/False)
    """
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        query = """
            INSERT INTO documents (year, type, created, creator, protected, file_path)
            VALUES (?, ?, ?, ?, ?, ?);
        """
        cur.execute(query, (
            year,
            doc_type,
            created,
            creator,
            int(protected),
            file_path
        ))
        con.commit()


def load_docs():
    with sqlite3.connect(DB_PATH) as con:
        cursor = con.cursor()
        cursor.execute("SELECT id, year, type, created, creator, protected, file_path FROM documents")
        result = cursor.fetchall()
    data = []
    for row in result:
        data.append(list(row))
    return data

def load_teachers():
    with sqlite3.connect(DB_PATH) as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM teachers")
        result = cursor.fetchall()
    return result

def load_starostas():
    with sqlite3.connect(DB_PATH) as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM startostas")
        result = cursor.fetchall()
    return result