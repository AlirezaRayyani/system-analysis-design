import pandas as pd
import sqlite3


class DBConverter:
    """
    Reads tables from a SQLite database and converts them to
    CSV files or pandas DataFrames.
    """

    ALLOWED_TABLES = ["transactions", "users", "logs"]

    def __init__(self, db_path: str): 
        self.db_path = db_path        

    def _validate_table(self, table_name: str) -> None:
        """
        Raises ValueError if table_name is not in ALLOWED_TABLES.
        Acts as the primary defense against unauthorized table access.
        """
        if table_name not in self.ALLOWED_TABLES:
            raise ValueError(
                f"Table '{table_name}' is not allowed. "
                f"Valid tables: {self.ALLOWED_TABLES}"
            )

    def _read_table(self, table_name: str) -> pd.DataFrame:
        """
        Reads a validated table from the SQLite database.

        Security note: table_name is validated against a strict whitelist
        before being interpolated into the query, mitigating SQL injection
        risk that parameterized queries cannot address for identifiers.
        """
        self._validate_table(table_name)

        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql(f"SELECT * FROM [{table_name}]", conn)

    def to_csv(
        self,
        table_name: str,
        output_path: str | None = None,
    ) -> None:
        """
        Exports a table to a UTF-8 CSV file.

        Args:
            table_name:  Name of the table to export.
            output_path: Destination path. Defaults to '<table_name>.csv'.
        """
        df   = self._read_table(table_name)
        path = output_path or f"{table_name}.csv"
        df.to_csv(path, index=False, encoding="utf-8-sig")

    def to_dataframe(self, table_name: str) -> pd.DataFrame:
        """
        Returns a table as a pandas DataFrame.

        Args:
            table_name: Name of the table to load.
        """
        return self._read_table(table_name)