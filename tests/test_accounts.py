"""Проверки пароля и SQL на временной схеме. Запуск: uv run python tests/test_accounts.py"""

import os
import sqlite3
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import Models.dbhandler as dbh
from View.appearance_logic import (
    AUTH_FAILED,
    EMPTY_NEW_PASSWORD,
    WRONG_CURRENT_PASSWORD,
    cabinet_password_failure,
    new_password_failure,
    registration_failure,
    registration_teacher_failure,
    resolve_registration_teacher,
)


def _seed_account_db():
    dbh.execute_query(
        """
        INSERT INTO teachers (
            last_name, first_name, middle_name, academic_degree, academic_title, email, phone
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        ("Иванов", "Иван", "Иванович", "к.т.н.", "доцент", "ivanov@example.com", "1"),
    )
    teacher_id = dbh.execute_query("SELECT id FROM teachers LIMIT 1", fetch=True)[0][0]
    dbh.execute_query(
        """
        INSERT INTO users (
            teacher_id, username, password, last_name, first_name, middle_name
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (teacher_id, "user", "secret", "Иванов", "Иван", "Иванович"),
    )
    dbh.execute_query(
        """
        INSERT INTO startostas (
            teacher_id, last_name, first_name, middle_name, group_num, email, phone
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (teacher_id, "Петров", "Пётр", "Петрович", "4411", "starosta@example.com", "2"),
    )
    dbh.insert_document(2026, "План", "2026.11.09", "user", "Saves/fixture.docx", 0)


@contextmanager
def account_db():
    """Временная база со схемой приложения. Пароль пользователя — открытый текст secret."""
    previous = dbh.DB_PATH
    with tempfile.TemporaryDirectory() as directory:
        dbh.DB_PATH = str(Path(directory) / "accounts.db")
        try:
            dbh.create_tables()
            _seed_account_db()
            yield
        finally:
            dbh.DB_PATH = previous


def test_hash_password_round_trip():
    stored = dbh.hash_password("secret")
    assert dbh.is_password_hash(stored)
    assert dbh.password_matches("secret", stored) is True
    assert dbh.password_matches("other", stored) is False


def test_plaintext_login_is_replaced_by_hash():
    with account_db():
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


def test_empty_new_password_is_refused():
    assert new_password_failure("", "") == EMPTY_NEW_PASSWORD
    assert cabinet_password_failure("secret", "secret", "", "") == EMPTY_NEW_PASSWORD


def test_wrong_current_password_is_refused():
    assert (
        cabinet_password_failure("secret", "nope", "new-pass", "new-pass")
        == WRONG_CURRENT_PASSWORD
    )


def test_password_change_accepts_current_and_new():
    assert cabinet_password_failure("secret", "secret", "new-pass", "new-pass") is None


def test_update_user_password_stores_hash():
    with account_db():
        username = dbh.execute_query("SELECT username FROM users LIMIT 1", fetch=True)[0][0]
        dbh.execute_query(
            "UPDATE users SET password = ? WHERE username = ?",
            ("secret", username),
        )
        dbh.update_user_password(username, "new-pass")
        stored = dbh.execute_query(
            "SELECT password FROM users WHERE username = ?",
            (username,),
            fetch=True,
        )[0][0]
        assert dbh.is_password_hash(stored)
        assert dbh.password_matches("new-pass", stored) is True
        assert dbh.password_matches("secret", stored) is False


def test_login_failure_message_is_shared():
    assert "логин" in AUTH_FAILED and "пароль" in AUTH_FAILED


def test_registration_without_code_is_refused():
    from unittest.mock import patch

    previous = os.environ.get("REGISTRATION_CODE")
    try:
        with patch("View.appearance_logic.load_local_env"):
            os.environ.pop("REGISTRATION_CODE", None)
            message = registration_failure("anything")
            assert message == "Регистрация недоступна: не задан код регистрации"
            os.environ["REGISTRATION_CODE"] = "test-code"
            assert registration_failure("wrong") == "Неправильный код регистрации"
            assert registration_failure("test-code") is None
    finally:
        if previous is None:
            os.environ.pop("REGISTRATION_CODE", None)
        else:
            os.environ["REGISTRATION_CODE"] = previous


def test_registration_needs_exactly_one_teacher():
    assert registration_teacher_failure([]) == "Преподаватель не найден в справочнике"
    assert registration_teacher_failure([("1",)]) is None
    message = registration_teacher_failure([("1",), ("2",)])
    assert message == "В справочнике несколько преподавателей с таким ФИО"


def test_reserved_name_from_env_skips_code():
    from unittest.mock import patch

    from View.appearance_logic import canonical_username

    previous_code = os.environ.get("REGISTRATION_CODE")
    previous_name = os.environ.get("RESERVED_ADMIN")
    refused = "Регистрация недоступна: не задан код регистрации"
    try:
        with patch("View.appearance_logic.load_local_env"):
            os.environ.pop("REGISTRATION_CODE", None)
            os.environ["RESERVED_ADMIN"] = "keeper"
            assert registration_failure("", "keeper") is None
            assert registration_failure("чужой-код", "Keeper") is None
            assert canonical_username("Keeper") == "keeper"
            assert registration_failure("", "admin") == refused
            os.environ["RESERVED_ADMIN"] = ""
            assert registration_failure("", "keeper") == refused
    finally:
        if previous_code is None:
            os.environ.pop("REGISTRATION_CODE", None)
        else:
            os.environ["REGISTRATION_CODE"] = previous_code
        if previous_name is None:
            os.environ.pop("RESERVED_ADMIN", None)
        else:
            os.environ["RESERVED_ADMIN"] = previous_name


def test_reserved_registration_creates_teacher_and_user():
    from unittest.mock import patch

    previous_name = os.environ.get("RESERVED_ADMIN")
    try:
        with patch("View.appearance_logic.load_local_env"):
            os.environ["RESERVED_ADMIN"] = "keeper"
            with account_db():
                before = dbh.execute_query("SELECT COUNT(*) FROM teachers", fetch=True)[0][0]
                teacher_id, failure = resolve_registration_teacher(
                    "Keeper", "Админов", "Админ", "Админович"
                )
                assert failure is None
                after = dbh.execute_query("SELECT COUNT(*) FROM teachers", fetch=True)[0][0]
                assert after == before + 1
                dbh.insert_user(
                    teacher_id, "keeper", "secret-admin", "Админов", "Админ", "Админович"
                )
                assert dbh.authenticate("keeper", "secret-admin") is True
                again, again_failure = resolve_registration_teacher(
                    "keeper", "Админов", "Админ", "Админович"
                )
                assert again_failure is None
                assert again == teacher_id
                unchanged = dbh.execute_query("SELECT COUNT(*) FROM teachers", fetch=True)[0][0]
                assert unchanged == after
    finally:
        if previous_name is None:
            os.environ.pop("RESERVED_ADMIN", None)
        else:
            os.environ["RESERVED_ADMIN"] = previous_name


def test_referenced_teacher_is_kept():
    with account_db():
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


def test_protected_document_stays_and_open_one_is_removed():
    with account_db():
        dbh.insert_document(2026, "План", "2026.11.09", "user", "Saves/stage-protected.docx", 1)
        dbh.insert_document(2026, "План", "2026.11.09", "user", "Saves/stage-open.docx", 0)
        protected_id = dbh.execute_query(
            "SELECT id FROM documents WHERE file_path = ?",
            ("Saves/stage-protected.docx",),
            fetch=True,
        )[0][0]
        open_id = dbh.execute_query(
            "SELECT id FROM documents WHERE file_path = ?",
            ("Saves/stage-open.docx",),
            fetch=True,
        )[0][0]
        before = dbh.execute_query("SELECT COUNT(*) FROM documents", fetch=True)[0][0]
        try:
            dbh.remove_document(protected_id)
            raise AssertionError("защищённый документ не должен удаляться")
        except sqlite3.IntegrityError:
            pass
        kept = dbh.select_document_by_id(protected_id)
        assert kept and kept[0][5] == 1
        dbh.remove_document(open_id)
        assert dbh.select_document_by_id(open_id) == []
        dbh.remove_document("1 OR 1=1")
        after = dbh.execute_query("SELECT COUNT(*) FROM documents", fetch=True)[0][0]
        assert after == before - 1


def test_document_id_is_a_parameter():
    with account_db():
        before = dbh.execute_query("SELECT COUNT(*) FROM documents", fetch=True)[0][0]
        dbh.remove_document("1 OR 1=1")
        after = dbh.execute_query("SELECT COUNT(*) FROM documents", fetch=True)[0][0]
        assert before == after
        assert before > 0


def test_blank_teacher_email_is_stored_as_null():
    with account_db():
        dbh.insert_teacher("Один", "Иван", "Иванович", "", "", "", "3")
        dbh.insert_teacher("Два", "Пётр", "Петрович", "", "", "   ", "4")
        rows = dbh.execute_query(
            "SELECT email FROM teachers WHERE last_name IN (?, ?)",
            ("Один", "Два"),
            fetch=True,
        )
        assert [row[0] for row in rows] == [None, None]
        teacher_id = dbh.execute_query(
            "SELECT id FROM teachers WHERE last_name = ?",
            ("Один",),
            fetch=True,
        )[0][0]
        dbh.update_teacher(
            teacher_id, ["Один", "Иван", "Иванович", "", "", "Kept@Example.com", "3"]
        )
        stored = dbh.execute_query(
            "SELECT email FROM teachers WHERE id = ?", (teacher_id,), fetch=True
        )[0][0]
        assert stored == "Kept@Example.com"
        try:
            dbh.insert_teacher(
                "Три", "Иван", "Иванович", "", "", "ivanov@example.com", "5"
            )
            raise AssertionError("занятый адрес должен отказать")
        except sqlite3.IntegrityError:
            pass


def test_remembered_username_is_stored_outside_the_database():
    from window_support import (
        clear_remembered_username,
        read_remembered_username,
        save_remembered_username,
    )

    with tempfile.TemporaryDirectory() as directory:
        assert read_remembered_username(directory) is None
        save_remembered_username("second-user", directory)
        stored = (Path(directory) / "remembered_username").read_text(encoding="utf-8")
        assert stored == "second-user"
        assert "pass" not in stored
        assert read_remembered_username(directory) == "second-user"
        clear_remembered_username(directory)
        assert not (Path(directory) / "remembered_username").exists()
        assert read_remembered_username(directory) is None


def main():
    test_hash_password_round_trip()
    test_plaintext_login_is_replaced_by_hash()
    test_empty_new_password_is_refused()
    test_wrong_current_password_is_refused()
    test_password_change_accepts_current_and_new()
    test_update_user_password_stores_hash()
    test_login_failure_message_is_shared()
    test_registration_without_code_is_refused()
    test_registration_needs_exactly_one_teacher()
    test_referenced_teacher_is_kept()
    test_protected_document_stays_and_open_one_is_removed()
    test_document_id_is_a_parameter()
    test_blank_teacher_email_is_stored_as_null()
    test_remembered_username_is_stored_outside_the_database()
    print("account-checks-ok")


if __name__ == "__main__":
    main()
