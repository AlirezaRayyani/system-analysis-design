import sqlite3
import tempfile
import os

import pandas as pd
import pytest

from codes.db_converter import DBConverter


# ── fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def tmp_db(tmp_path) -> str:
    """
    Creates a real temporary SQLite database with a 'transactions' table
    so tests are not mocked end-to-end.
    """
    db_path = str(tmp_path / "test.db")
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE transactions (
                id   INTEGER PRIMARY KEY,
                name TEXT,
                amount REAL
            )
        """)
        conn.executemany(
            "INSERT INTO transactions (name, amount) VALUES (?, ?)",
            [("Alice", 100.0), ("Bob", 200.0), ("Charlie", 300.0)],
        )
        # also create 'users' table (another allowed table)
        conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT)")
        conn.executemany(
            "INSERT INTO users (username) VALUES (?)",
            [("alice",), ("bob",)],
        )
    return db_path


@pytest.fixture
def converter(tmp_db) -> DBConverter:
    return DBConverter(tmp_db)


# ── __init__ ──────────────────────────────────────────────────────────────────

class TestInit:

    def test_db_path_stored_correctly(self, tmp_db):
        conv = DBConverter(tmp_db)
        assert conv.db_path == tmp_db

    def test_allowed_tables_unchanged(self):
        assert "transactions" in DBConverter.ALLOWED_TABLES
        assert "users"        in DBConverter.ALLOWED_TABLES
        assert "logs"         in DBConverter.ALLOWED_TABLES


# ── _validate_table ───────────────────────────────────────────────────────────

class TestValidateTable:

    def test_valid_table_does_not_raise(self, converter):
        converter._validate_table("transactions")   # no exception

    def test_invalid_table_raises_value_error(self, converter):
        with pytest.raises(ValueError):
            converter._validate_table("secret_data")

    def test_error_message_contains_table_name(self, converter):
        with pytest.raises(ValueError, match="secret_data"):
            converter._validate_table("secret_data")

    def test_sql_injection_attempt_is_blocked(self, converter):
        with pytest.raises(ValueError):
            converter._validate_table("transactions; DROP TABLE transactions;--")

    def test_case_sensitive_rejection(self, converter):
        # 'Transactions' (capital T) is NOT in the whitelist
        with pytest.raises(ValueError):
            converter._validate_table("Transactions")


# ── to_dataframe ──────────────────────────────────────────────────────────────

class TestToDataframe:

    def test_returns_dataframe(self, converter):
        result = converter.to_dataframe("transactions")
        assert isinstance(result, pd.DataFrame)

    def test_row_count_is_correct(self, converter):
        df = converter.to_dataframe("transactions")
        assert len(df) == 3

    def test_columns_are_present(self, converter):
        df = converter.to_dataframe("transactions")
        assert "name"   in df.columns
        assert "amount" in df.columns

    def test_values_are_correct(self, converter):
        df = converter.to_dataframe("transactions")
        assert set(df["name"]) == {"Alice", "Bob", "Charlie"}

    def test_invalid_table_raises(self, converter):
        with pytest.raises(ValueError):
            converter.to_dataframe("admin")

    def test_users_table_is_readable(self, converter):
        df = converter.to_dataframe("users")
        assert len(df) == 2


# ── to_csv ────────────────────────────────────────────────────────────────────

class TestToCsv:

    def test_creates_file_at_default_path(self, converter, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        converter.to_csv("transactions")
        assert os.path.exists(tmp_path / "transactions.csv")

    def test_creates_file_at_custom_path(self, converter, tmp_path):
        out = str(tmp_path / "output.csv")
        converter.to_csv("transactions", output_path=out)
        assert os.path.exists(out)

    def test_csv_has_correct_row_count(self, converter, tmp_path):
        out = str(tmp_path / "output.csv")
        converter.to_csv("transactions", output_path=out)
        df = pd.read_csv(out)
        assert len(df) == 3

    def test_csv_has_correct_columns(self, converter, tmp_path):
        out = str(tmp_path / "output.csv")
        converter.to_csv("transactions", output_path=out)
        df = pd.read_csv(out)
        assert "name"   in df.columns
        assert "amount" in df.columns

    def test_csv_encoding_is_utf8_sig(self, converter, tmp_path):
        out = str(tmp_path / "output.csv")
        converter.to_csv("transactions", output_path=out)
        with open(out, "rb") as f:
            bom = f.read(3)
        # UTF-8-sig starts with BOM: EF BB BF
        assert bom == b"\xef\xbb\xbf"

    def test_invalid_table_raises_before_writing(self, converter, tmp_path):
        out = str(tmp_path / "should_not_exist.csv")
        with pytest.raises(ValueError):
            converter.to_csv("forbidden_table", output_path=out)
        assert not os.path.exists(out)
