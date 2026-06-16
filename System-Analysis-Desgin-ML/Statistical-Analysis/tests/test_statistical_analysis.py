import pytest
import pandas as pd
from unittest.mock import patch
from codes.statistical_analysis import StatisticalAnalysis




@pytest.fixture
def analysis(sample_df):
    return StatisticalAnalysis(sample_df)



class TestKpiSummary:

    def test_returns_correct_keys(self, analysis):
        result = analysis.kpi_summary(1)
        assert set(result.keys()) == {"income", "expense", "net", "tx_count"}

    def test_income_is_correct(self, analysis):
        assert analysis.kpi_summary(1)["income"] == 10_000

    def test_expense_is_correct(self, analysis):
        # 1200+300+1200+500+200 = 3400
        assert analysis.kpi_summary(1)["expense"] == 3_400

    def test_net_balance(self, analysis):
        kpi = analysis.kpi_summary(1)
        assert kpi["net"] == kpi["income"] - kpi["expense"]

    def test_tx_count(self, analysis):
        assert analysis.kpi_summary(1)["tx_count"] == 7

    def test_unknown_user_returns_zeros(self, analysis):
        result = analysis.kpi_summary(999)
        assert result["income"]   == 0
        assert result["expense"]  == 0
        assert result["net"]      == 0
        assert result["tx_count"] == 0


class TestSavingRate:

    def test_saving_rate_value(self, analysis):
        # net = 6600, income = 10000  →  66%
        assert analysis.saving_rate(1) == pytest.approx(66.0, rel=1e-2)

    def test_zero_income_returns_zero(self, analysis):
        # user 2 has no income
        assert analysis.saving_rate(2) == 0.0

    def test_no_expense_returns_100(self, analysis):
        # user 3 has income only
        assert analysis.saving_rate(3) == pytest.approx(100.0)

    def test_return_type_is_float(self, analysis):
        assert isinstance(analysis.saving_rate(1), float)



class TestAverageExpenseLastNDays:

    def test_returns_float(self, analysis):
        result = analysis.average_expense_last_n_days(1, n_days=7)
        assert isinstance(result, float)

    def test_no_expense_user_returns_nan_or_zero(self, analysis):
        # user 3 has no expenses → resample produces no rows → mean is NaN
        result = analysis.average_expense_last_n_days(3, n_days=7)
        assert result != result or result == 0.0  # NaN or 0


class TestExpenseByCategories:

    def test_returns_required_keys(self, analysis):
        result = analysis.expense_by_categories(1)
        assert "expense_by_category" in result
        assert "category_share"      in result
        assert "transaction_count"   in result

    def test_categories_are_correct(self, analysis):
        cats = set(analysis.expense_by_categories(1)["expense_by_category"].keys())
        assert cats == {"Rent", "Food", "Transport"}

    def test_shares_sum_to_100(self, analysis):
        shares = analysis.expense_by_categories(1)["category_share"]
        assert sum(shares.values()) == pytest.approx(100.0, rel=1e-2)

    def test_no_expense_user_returns_empty_dicts(self, analysis):
        result = analysis.expense_by_categories(3)
        assert result["expense_by_category"] == {}

    def test_transaction_counts_are_correct(self, analysis):
        counts = analysis.expense_by_categories(1)["transaction_count"]
        # Rent appears twice, Food twice, Transport once
        assert counts["Rent"]      == 2
        assert counts["Food"]      == 2
        assert counts["Transport"] == 1


class TestIncomeLastNDays:

    def test_no_recent_income_returns_zero(self, analysis):
        # All transactions are in 2024; window of 7 days from "now" won't match
        result = analysis.income_last_n_days(1, days=7)
        assert result == 0.0

    def test_large_window_captures_all_income(self, analysis):
        # Use a huge window so all 2024 records fall inside
        with patch("statistical_analysis.pd.Timestamp") as mock_ts:
            mock_ts.now.return_value = pd.Timestamp("2024-03-01")
            result = analysis.income_last_n_days(1, days=365)
        assert result == pytest.approx(10_000)

    def test_return_type_is_float(self, analysis):
        assert isinstance(analysis.income_last_n_days(1), float)



class TestIncomeStabilityIndex:

    def test_stable_income_returns_low_isi(self, analysis):
        # User 1 earns exactly 5000 each month → std=0 → ISI=0
        assert analysis.income_stability_index(1) == pytest.approx(0.0, abs=1e-2)

    def test_zero_income_returns_zero(self, analysis):
        assert analysis.income_stability_index(2) == 0.0

    def test_return_type_is_float(self, analysis):
        assert isinstance(analysis.income_stability_index(1), float)




class TestExpenseToIncomeRatio:

    def test_ratio_value(self, analysis):
        # expense=3400, income=10000 → 34%
        assert analysis.expense_to_income_ratio(1) == pytest.approx(34.0, rel=1e-2)

    def test_zero_income_returns_zero(self, analysis):
        assert analysis.expense_to_income_ratio(2) == 0.0

    def test_no_expense_returns_zero(self, analysis):
        assert analysis.expense_to_income_ratio(3) == pytest.approx(0.0)

    def test_return_type_is_float(self, analysis):
        assert isinstance(analysis.expense_to_income_ratio(1), float)
