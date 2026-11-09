import os
import sqlite3

import bcrypt as bcrypt_lib

# bcrypt 4.x убрал __about__, а passlib 1.7.4 всё ещё читает его при первом вызове.
if not hasattr(bcrypt_lib, "__about__"):

    class _BcryptAbout:
        __version__ = getattr(bcrypt_lib, "__version__", "4")

    bcrypt_lib.__about__ = _BcryptAbout()

from passlib.hash import bcrypt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "DB", "maindatabase.db")


def is_password_hash(stored):
    return isinstance(stored, str) and stored.startswith(("$2a$", "$2b$", "$2y$"))


def hash_password(password):
    return bcrypt.hash(password)


def password_matches(password, stored):
    if stored is None:
        return False
    stored = str(stored)
    if is_password_hash(stored):
        return bcrypt.verify(password, stored)
    return password == stored


def execute_query(query, params=(), fetch=False, many=False):
    con = sqlite3.connect(DB_PATH)
    try:
        con.execute("PRAGMA foreign_keys = ON")
        cur = con.cursor()
        if many:
            cur.executemany(query, params)
        else:
            cur.execute(query, params)
        con.commit()
        if fetch:
            return cur.fetchall()
    finally:
        con.close()


def create_tables():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    create_docs_table()
    create_teachers_table()
    create_starosta_table()
    create_users_table()


def create_starosta_table():
    query = """
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
    """
    execute_query(query)


def create_teachers_table():
    query = """
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
    """
    execute_query(query)


def create_docs_table():
    query = """
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER,
            type TEXT,
            created TEXT,
            creator TEXT,
            protected INTEGER,
            file_path TEXT
        );
    """
    execute_query(query)


def create_users_table():
    query = """
        CREATE TABLE IF NOT EXISTS users (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             teacher_id INTEGER,
             username VARCHAR(50) UNIQUE,
             password TEXT NOT NULL,
             last_name VARCHAR(50) NOT NULL,
             first_name VARCHAR(50) NOT NULL,
             middle_name VARCHAR(50),
             is_remembered INTEGER DEFAULT 0,
             FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE SET NULL
        );
    """
    execute_query(query)


def update_teacher(id, data):
    query = """
        UPDATE teachers
        SET last_name = ?,
            first_name = ?,
            middle_name = ?,
            academic_degree = ?,
            academic_title = ?,
            email = ?,
            phone = ?
        WHERE id = ?
    """
    execute_query(query, tuple(data) + (id,))


def teacher_has_references(teacher_id):
    rows = execute_query(
        """
        SELECT 1 FROM startostas WHERE teacher_id = ?
        UNION
        SELECT 1 FROM users WHERE teacher_id = ?
        LIMIT 1
        """,
        (teacher_id, teacher_id),
        fetch=True,
    )
    return bool(rows)


def remove_teacher(id):
    if teacher_has_references(id):
        raise sqlite3.IntegrityError(
            "Нельзя удалить преподавателя: на него ссылаются староста или пользователь"
        )
    execute_query("DELETE FROM teachers WHERE id = ?", (id,))


def remove_document(id):
    execute_query("DELETE FROM documents WHERE id = ?", (id,))


def defend_document(id, status):
    query = """
        UPDATE documents
        SET protected = ?
        WHERE id = ?
    """
    execute_query(query, (status, id))


def remove_user(username):
    query = "DELETE FROM users WHERE username = ?"
    execute_query(query, (username,))


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
    params = (teacher_id, username, hash_password(password), l_name, f_name, m_name)
    execute_query(query, params)


def insert_starosta(teacher_id, l_name, f_name, m_name, group, email, phone):
    query = """
        INSERT INTO startostas (teacher_id, last_name, first_name, middle_name, group_num, email, phone)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """
    params = (teacher_id, l_name, f_name, m_name, group, email, phone)
    execute_query(query, params)


def update_starosta(id, data):
    query = """
        UPDATE startostas
        SET teacher_id = ?,
            last_name = ?,
            first_name = ?,
            middle_name = ?,
            group_num = ?,
            email = ?,
            phone = ?
        WHERE id = ?
    """
    execute_query(query, tuple(data) + (id,))


def remove_starosta(id):
    execute_query("DELETE FROM startostas WHERE id = ?", (id,))


def insert_document(
    year: int, doc_type: str, created: str, creator: str, file_path: str, protected: int = 0
):
    query = """
        INSERT INTO documents (year, type, created, creator, protected, file_path)
        VALUES (?, ?, ?, ?, ?, ?);
    """
    params = (year, doc_type, created, creator, int(protected), file_path)
    execute_query(query, params)


def select_teacher_by_name(l_name, f_name, m_name):
    query = """SELECT * FROM teachers
        WHERE last_name = ? AND first_name = ? AND middle_name = ?
    """
    params = (l_name, f_name, m_name)
    return execute_query(query, params=params, fetch=True)


def select_teacher_by_id(id):
    query = """SELECT * FROM teachers
        WHERE id = ?
    """
    return execute_query(query, (id,), fetch=True)


def select_user_by_username(username):
    query = """SELECT * FROM users
        WHERE username = ?
    """
    return execute_query(query, (username,), fetch=True)


def select_remembered_user():
    query = """SELECT * FROM users
        WHERE is_remembered = 1
    """
    return execute_query(query, fetch=True)


def update_user_password(username, new_password):
    query = """
        UPDATE users
        SET password = ?
        WHERE username = ?
    """
    execute_query(query, (hash_password(new_password), username))


def authenticate(username, password):
    """True, если пара верна. Открытый старый пароль после успеха заменяется хешем."""
    users = select_user_by_username(username)
    if not users:
        return False
    stored = users[0][3]
    if not password_matches(password, stored):
        return False
    if not is_password_hash(str(stored)):
        update_user_password(username, password)
    return True


def update_remember_status(username, status):
    if int(status):
        execute_query("UPDATE users SET is_remembered = 0 WHERE username != ?", (username,))
    execute_query(
        """
        UPDATE users
        SET is_remembered = ?
        WHERE username = ?
        """,
        (int(status), username),
    )


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
