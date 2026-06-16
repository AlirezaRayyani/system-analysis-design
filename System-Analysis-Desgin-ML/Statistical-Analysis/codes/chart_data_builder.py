import pandas as pd
from base_user_data import BaseUserData


class ChartDataBuilder(BaseUserData):

    def expense_category_pie(self, user_id: int | str) -> dict:
        """
        Data for a pie chart of expenses grouped by category.

        Returns:
            Chart.js-compatible dict with labels and datasets.
        """
        data = self._prepare_user_data(user_id)

        grouped = (
            data.loc[data["Transaction Kind"] == "Expense", ["Category", "Amount"]]
            .groupby("Category")["Amount"]
            .sum()
        )

        return {
            "labels": grouped.index.tolist(),
            "datasets": [{"label": "Expenses", "data": grouped.tolist()}],
        }

    def monthly_income_expense_line(self, user_id: int | str) -> dict:
        """
        Data for a line chart comparing monthly income vs expense.

        Returns:
            Chart.js-compatible dict with labels and two datasets.
        """
        data = self._prepare_user_data(user_id)

        monthly = (
            data.groupby(
                [pd.Grouper(key="Date Time", freq="ME"), "Transaction Kind"]
            )["Amount"]
            .sum()
            .unstack(fill_value=0)
        )

        empty = pd.Series(0, index=monthly.index)

        return {
            "labels": [d.strftime("%Y-%m") for d in monthly.index],
            "datasets": [
                {"label": "Income",  "data": monthly.get("Income",  empty).tolist()},
                {"label": "Expense", "data": monthly.get("Expense", empty).tolist()},
            ],
        }

    def cashflow_trend_line(self, user_id: int | str) -> dict:
        """
        Data for a line chart of monthly net cash flow (income - expense).

        Returns:
            Chart.js-compatible dict with labels and one dataset.
        """
        data = self._prepare_user_data(user_id)

        monthly = (
            data.groupby(
                [pd.Grouper(key="Date Time", freq="ME"), "Transaction Kind"]
            )["Amount"]
            .sum()
            .unstack(fill_value=0)
        )

        empty = pd.Series(0, index=monthly.index)
        net   = monthly.get("Income", empty) - monthly.get("Expense", empty)

        return {
            "labels": [d.strftime("%Y-%m") for d in monthly.index],
            "datasets": [{"label": "Net Cash Flow", "data": net.tolist()}],
        }

    def top_expense_categories_bar(
        self, user_id: int | str, top_n: int = 5
    ) -> dict:
        """
        Data for a bar chart of the top N expense categories.

        Args:
            top_n: Number of top categories to return. Must be >= 1.

        Returns:
            Chart.js-compatible dict with labels and one dataset.

        Raises:
            ValueError: If top_n is less than 1.
        """
        if top_n < 1:
            raise ValueError("top_n must be at least 1.")

        data = self._prepare_user_data(user_id)

        grouped = (
            data.loc[data["Transaction Kind"] == "Expense", ["Category", "Amount"]]
            .groupby("Category")["Amount"]
            .sum()
            .sort_values(ascending=False)
            .head(top_n)
        )

        return {
            "labels": grouped.index.tolist(),
            "datasets": [{"label": "Expense Amount", "data": grouped.tolist()}],
        }

    def monthly_transaction_count_bar(self, user_id: int | str) -> dict:
        """
        Data for a bar chart of monthly transaction counts.

        Returns:
            Chart.js-compatible dict with labels and one dataset.
        """
        data = self._prepare_user_data(user_id)

        monthly = (
            data.set_index("Date Time")
            .resample("ME")
            .size()
        )

        return {
            "labels": [d.strftime("%Y-%m") for d in monthly.index],
            "datasets": [{"label": "Transactions", "data": monthly.tolist()}],
        }