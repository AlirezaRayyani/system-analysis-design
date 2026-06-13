import pandas as pd
import pytest



SAMPLE_ROWS = [
    # user 1 – normal activity
    {"User ID": 1, "Date Time": "2024-01-15", "Transaction Kind": "Income",  "Amount": 5000, "Category": "Salary"},
    {"User ID": 1, "Date Time": "2024-01-20", "Transaction Kind": "Expense", "Amount": 1200, "Category": "Rent"},
    {"User ID": 1, "Date Time": "2024-01-25", "Transaction Kind": "Expense", "Amount":  300, "Category": "Food"},
    {"User ID": 1, "Date Time": "2024-02-15", "Transaction Kind": "Income",  "Amount": 5000, "Category": "Salary"},
    {"User ID": 1, "Date Time": "2024-02-20", "Transaction Kind": "Expense", "Amount": 1200, "Category": "Rent"},
    {"User ID": 1, "Date Time": "2024-02-22", "Transaction Kind": "Expense", "Amount":  500, "Category": "Food"},
    {"User ID": 1, "Date Time": "2024-02-28", "Transaction Kind": "Expense", "Amount":  200, "Category": "Transport"},
    # user 2 – zero income edge case
    {"User ID": 2, "Date Time": "2024-01-10", "Transaction Kind": "Expense", "Amount":  400, "Category": "Food"},
    # user 3 – income only, no expenses
    {"User ID": 3, "Date Time": "2024-01-05", "Transaction Kind": "Income",  "Amount": 3000, "Category": "Freelance"},
]


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """Base DataFrame used across all test modules."""
    return pd.DataFrame(SAMPLE_ROWS)
