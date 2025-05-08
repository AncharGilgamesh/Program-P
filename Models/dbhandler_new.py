import os
import sqlite3
from PySide6.QtCore import QDate

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'DB', 'maindatabase.db')

def execute_query(query, params=(), fetch=False, many=False):
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        if many:
            cur.executemany(query, params)
        else:
            cur.execute(query, params)
        con.commit()
        if fetch:
            return cur.fetchall()

def create_tables():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    create_docs_table()
    create_teachers_table()
    create_starosta_table()
    create_users_table()

def create_starosta_table():
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
    execute_query(query)

def create_teachers_table():
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
    execute_query(query)

def create_docs_table():
    query = ("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER,
            type TEXT,
            created TEXT,
            creator TEXT,
            protected INTEGER,
            file_path TEXT
        );
    """)
    execute_query(query)

def create_users_table():
    query = ("""
        CREATE TABLE IF NOT EXISTS users (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             teacher_id INTEGER,
             username VARCHAR(50) UNIQUE,
             password VARCHAR(50) NOT NULL,
             last_name VARCHAR(50) NOT NULL,
             first_name VARCHAR(50) NOT NULL,
             middle_name VARCHAR(50),
             is_remembered INTEGER DEFAULT 0,
             FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE SET NULL
        );
    """)
    execute_query(query)

def insert_user(data):
    query = """
        INSERT INTO startostas (teacher_id, username, password, last_name, first_name, middle_name)
        VALUES (?, ?, ?, ?, ?, ?);
    """
    execute_query(query, data) 

def update_teacher(id, data):
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
    """).format(id)
    execute_query(query, data)

def remove_teacher(id):
    query = "DELETE FROM teachers WHERE id = {}".format(id)
    execute_query(query)

def insert_teacher(l_name, f_name, m_name, a_degree, a_title, email, phone):
    query = """
        INSERT INTO teachers (last_name, first_name, middle_name, academic_degree, academic_title, email, phone)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """
    params = (l_name, f_name, m_name, a_degree, a_title, email, phone)
    execute_query(query, params)

def insert_user(teacher_id, username, password, l_name, f_name, m_name):
    query = """
        INSERT INTO users (teacher_id, username, password, last_name, first_name, middle_name)
        VALUES (?, ?, ?, ?, ?, ?);
    """
    params = (teacher_id, username, password, l_name, f_name, m_name)
    execute_query(query, params)

def insert_starosta(teacher_id, l_name, f_name, m_name, group, email, phone):
    query = """
        INSERT INTO startostas (teacher_id, last_name, first_name, middle_name, group_num, email, phone)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """
    params = (teacher_id, l_name, f_name, m_name, group, email, phone)
    execute_query(query, params)

def update_starosta(id, data):
    query = ("""
        UPDATE startostas
        SET teacher_id = ?,
            last_name = ?,
            first_name = ?,
            middle_name = ?,
            group_num = ?,
            email = ?,
            phone = ?
        WHERE id = {}
    """).format(id)
    execute_query(query, data)

def remove_starosta(id):
    query = "DELETE FROM startostas WHERE id = {}".format(id)
    execute_query(query)

def insert_document(year: int, doc_type: str, created: str, creator: str, file_path: str, protected: bool = False):
    query = """
        INSERT INTO documents (year, type, created, creator, protected, file_path)
        VALUES (?, ?, ?, ?, ?, ?);
    """
    params = (year, doc_type, created, creator, int(protected), file_path)
    execute_query(query, params)

def select_teacher_by_name(l_name, f_name, m_name):
    query = ("""SELECT * FROM teachers
        WHERE last_name = ? AND first_name = ? AND middle_name = ?
    """)
    params = (l_name, f_name, m_name)
    return execute_query(query, params=params, fetch=True)

def select_user_by_username(username):
    query = ("""SELECT * FROM users
        WHERE username = ?
    """)
    return execute_query(query, (username,), fetch=True)

def update_user_password(username, new_password):
    query = ("""
        UPDATE users
        SET password = ?
        WHERE username = {}
    """).format(username)
    execute_query(query, (new_password,))

def load_docs():
    query = "SELECT id, year, type, created, creator, protected, file_path FROM documents"
    result = execute_query(query, fetch=True)
    return [list(row) for row in result]

def load_teachers():
    query = "SELECT * FROM teachers"
    return execute_query(query, fetch=True)

def load_starostas():
    query = "SELECT * FROM startostas"
    return execute_query(query, fetch=True)

