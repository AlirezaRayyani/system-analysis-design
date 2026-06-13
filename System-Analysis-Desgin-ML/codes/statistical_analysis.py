import pandas as pd
from base_user_data import BaseUserData


class StatisticalAnalysis(BaseUserData):


    def _total_income(self, user_data: pd.DataFrame) -> float:
        """Returns total earned income from a prepared user DataFrame."""
        return float(
            user_data.loc[
                user_data["Transaction Kind"] == "Income", "Amount"
            ].sum()
        )

    def _total_expense(self, user_data: pd.DataFrame) -> float:
        """Returns total spent expense from a prepared user DataFrame."""
        return float(
            user_data.loc[
                user_data["Transaction Kind"] == "Expense", "Amount"
            ].sum()
        )


    def kpi_summary(self, user_id: int | str) -> dict:
        """
        Computes key financial metrics:
        total income, total expense, net balance, transaction count.

        Returns:
            dict with keys: income, expense, net, tx_count.
        """
        user_data = self._prepare_user_data(user_id)
        income  = self._total_income(user_data)
        expense = self._total_expense(user_data)

        return {
            "income":    income,
            "expense":   expense,
            "net":       income - expense,
            "tx_count":  len(user_data),
        }

    def saving_rate(self, user_id: int | str) -> float:
        """
        Saving rate formula: ((income - expense) / income) * 100

        Returns:
            0.0 if income == 0, otherwise saving rate as a percentage.
        """
        user_data = self._prepare_user_data(user_id)
        income  = self._total_income(user_data)
        expense = self._total_expense(user_data)

        if income == 0:
            return 0.0

        return round(((income - expense) / income) * 100, 2)

    def average_expense_last_n_days(
        self, user_id: int | str, n_days: int = 7
    ) -> float:
        """
        Average daily expense over the last n days.
        Formula: sum_of_expenses_in_period / n_days

        Returns:
            Rolling average of daily expenses over the specified period.
        """
        user_data = self._prepare_user_data(user_id)

        expenses = (
            user_data[user_data["Transaction Kind"] == "Expense"]
            .set_index("Date Time")
        )

        daily = expenses["Amount"].resample("D").sum()
        return round(float(daily.tail(n_days).mean()), 2)

    def expense_by_categories(self, user_id: int | str) -> dict:
        """
        Expense breakdown by category: total amount, share (%), tx count.

        Returns:
            dict with keys: expense_by_category, category_share,
            transaction_count.
        """
        user_data = self._prepare_user_data(user_id)

        expenses = user_data.loc[
            user_data["Transaction Kind"] == "Expense",
            ["Amount", "Category"],
        ]

        grouped = expenses.groupby("Category").agg(
            total_amount=("Amount", "sum"),
            tx_count=("Amount", "count"),
        )

        tot_expense = grouped["total_amount"].sum()
        grouped["share_percent"] = (
            (grouped["total_amount"] / tot_expense * 100).round(2)
            if tot_expense != 0
            else 0.0
        )

        return {
            "expense_by_category": grouped["total_amount"].to_dict(),
            "category_share":      grouped["share_percent"].to_dict(),
            "transaction_count":   grouped["tx_count"].to_dict(),
        }

    def income_last_n_days(self, user_id: int | str, days: int = 30) -> float:
        """
        Total income earned during the last n days.

        Uses timezone-naive now() to match the tz-localize(None) applied
        in _prepare_user_data, avoiding comparison errors.

        Returns:
            Sum of income amounts in the specified window.
        """
        user_data = self._prepare_user_data(user_id)

        cutoff = pd.Timestamp.now(tz=None) - pd.Timedelta(days=days)

        income = user_data.loc[
            (user_data["Transaction Kind"] == "Income")
            & (user_data["Date Time"] >= cutoff),
            "Amount",
        ]

        return float(income.sum())

    def income_stability_index(self, user_id: int | str) -> float:
        """
        Income Stability Index (ISI) via coefficient of variation (CV).
        Formula: (std(monthly_income) / mean(monthly_income)) * 100

        Returns:
            0.0 if mean monthly income is zero, otherwise CV as a percentage.
        """
        user_data = self._prepare_user_data(user_id)

        monthly_income = (
            user_data[user_data["Transaction Kind"] == "Income"]
            .set_index("Date Time")
            .resample("ME")["Amount"]
            .sum()
        )

        mean_income = monthly_income.mean()
        if mean_income == 0:
            return 0.0

        cv = (monthly_income.std() / mean_income) * 100
        return round(float(cv), 2)

    def expense_to_income_ratio(self, user_id: int | str) -> float:
        """
        Expense to Income Ratio (EIR).
        Formula: (total_expense / total_income) * 100

        Returns:
            0.0 if total income is zero, otherwise EIR as a percentage.
        """
        user_data  = self._prepare_user_data(user_id)
        tot_income  = self._total_income(user_data)
        tot_expense = self._total_expense(user_data)

        if tot_income == 0:
            return 0.0

        return round((tot_expense / tot_income) * 100, 2)