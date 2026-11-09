"""Проверки пароля и SQL на копии базы. Запуск: uv run python tests/test_accounts.py"""

import os
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import Models.dbhandler_new as dbh
from View.appearance_logic import AUTH_FAILED, registration_failure

SOURCE_DB = Path(__file__).resolve().parents[1] / "DB" / "maindatabase.db"


def use_copy(directory):
    copy_path = Path(directory) / "maindatabase.db"
    shutil.copy(SOURCE_DB, copy_path)
    dbh.DB_PATH = str(copy_path)
    return copy_path


def test_plaintext_login_is_replaced_by_hash():
    with tempfile.TemporaryDirectory() as directory:
        use_copy(directory)
        row = dbh.execute_query(
            "SELECT username, password FROM users LIMIT 1", fetch=True
        )[0]
        username, original = row
        assert not dbh.is_password_hash(original)
        assert dbh.authenticate(username, original) is True
        stored = dbh.execute_query(
            "SELECT password FROM users WHERE username = ?", (username,), fetch=True
        )[0][0]
        assert stored != original
        assert dbh.is_password_hash(stored)
        assert dbh.authenticate(username, original) is True
        assert dbh.authenticate(username, original + "x") is False
        assert dbh.authenticate(username + "-missing", original) is False


def test_login_failure_message_is_shared():
    assert "логин" in AUTH_FAILED and "пароль" in AUTH_FAILED


def test_registration_without_code_is_refused():
    os.environ.pop("REGISTRATION_CODE", None)
    message = registration_failure("anything")
    assert message == "Регистрация недоступна: не задан код регистрации"
    os.environ["REGISTRATION_CODE"] = "test-code"
    try:
        assert registration_failure("wrong") == "Неправильный код регистрации"
        assert registration_failure("test-code") is None
    finally:
        os.environ.pop("REGISTRATION_CODE", None)


def test_referenced_teacher_is_kept():
    with tempfile.TemporaryDirectory() as directory:
        use_copy(directory)
        teacher_id = dbh.execute_query(
            """
            SELECT teacher_id FROM startostas WHERE teacher_id IS NOT NULL
            UNION
            SELECT teacher_id FROM users WHERE teacher_id IS NOT NULL
            LIMIT 1
            """,
            fetch=True,
        )[0][0]
        before = dbh.execute_query(
            "SELECT COUNT(*) FROM teachers WHERE id = ?", (teacher_id,), fetch=True
        )[0][0]
        try:
            dbh.remove_teacher(teacher_id)
            raise AssertionError("удаление связанного преподавателя должно отказать")
        except sqlite3.IntegrityError:
            pass
        after = dbh.execute_query(
            "SELECT COUNT(*) FROM teachers WHERE id = ?", (teacher_id,), fetch=True
        )[0][0]
        assert before == after == 1


def test_document_id_is_a_parameter():
    with tempfile.TemporaryDirectory() as directory:
        use_copy(directory)
        before = dbh.execute_query("SELECT COUNT(*) FROM documents", fetch=True)[0][0]
        dbh.remove_document("1 OR 1=1")
        after = dbh.execute_query("SELECT COUNT(*) FROM documents", fetch=True)[0][0]
        assert before == after
        assert before > 0


def test_remember_flag_stays_on_one_user():
    with tempfile.TemporaryDirectory() as directory:
        use_copy(directory)
        teacher_id = dbh.execute_query(
            "SELECT id FROM teachers LIMIT 1", fetch=True
        )[0][0]
        dbh.insert_user(teacher_id, "second-user", "second-pass", "А", "Б", "В")
        dbh.update_remember_status("second-user", 1)
        remembered = dbh.execute_query(
            "SELECT username FROM users WHERE is_remembered = 1", fetch=True
        )
        assert [row[0] for row in remembered] == ["second-user"]


def main():
    test_plaintext_login_is_replaced_by_hash()
    test_login_failure_message_is_shared()
    test_registration_without_code_is_refused()
    test_referenced_teacher_is_kept()
    test_document_id_is_a_parameter()
    test_remember_flag_stays_on_one_user()
    print("account-checks-ok")


if __name__ == "__main__":
    main()
