import pytest
from codes.chart_data_builder import ChartDataBuilder



@pytest.fixture
def builder(sample_df):
    return ChartDataBuilder(sample_df)



class TestExpenseCategoryPie:

    def test_returns_labels_and_datasets(self, builder):
        result = builder.expense_category_pie(1)
        assert "labels"   in result
        assert "datasets" in result

    def test_labels_are_categories(self, builder):
        labels = set(builder.expense_category_pie(1)["labels"])
        assert labels == {"Rent", "Food", "Transport"}

    def test_dataset_length_matches_labels(self, builder):
        result = builder.expense_category_pie(1)
        assert len(result["labels"]) == len(result["datasets"][0]["data"])

    def test_data_values_are_positive(self, builder):
        data = builder.expense_category_pie(1)["datasets"][0]["data"]
        assert all(v > 0 for v in data)

    def test_no_expense_user_returns_empty(self, builder):
        result = builder.expense_category_pie(3)
        assert result["labels"] == []

    def test_unknown_user_returns_empty(self, builder):
        result = builder.expense_category_pie(999)
        assert result["labels"] == []



class TestMonthlyIncomeExpenseLine:

    def test_returns_required_keys(self, builder):
        result = builder.monthly_income_expense_line(1)
        assert "labels"   in result
        assert "datasets" in result

    def test_two_datasets_returned(self, builder):
        result = builder.monthly_income_expense_line(1)
        assert len(result["datasets"]) == 2

    def test_dataset_labels(self, builder):
        dataset_labels = {
            d["label"] for d in builder.monthly_income_expense_line(1)["datasets"]
        }
        assert dataset_labels == {"Income", "Expense"}

    def test_labels_are_year_month_format(self, builder):
        labels = builder.monthly_income_expense_line(1)["labels"]
        for label in labels:
            assert len(label) == 7          # "YYYY-MM"
            assert label[4] == "-"

    def test_data_length_matches_labels(self, builder):
        result = builder.monthly_income_expense_line(1)
        n = len(result["labels"])
        for ds in result["datasets"]:
            assert len(ds["data"]) == n

    def test_user_1_has_two_months(self, builder):
        labels = builder.monthly_income_expense_line(1)["labels"]
        assert len(labels) == 2



class TestCashflowTrendLine:

    def test_returns_required_keys(self, builder):
        result = builder.cashflow_trend_line(1)
        assert "labels"   in result
        assert "datasets" in result

    def test_single_dataset(self, builder):
        assert len(builder.cashflow_trend_line(1)["datasets"]) == 1

    def test_dataset_label_is_net_cash_flow(self, builder):
        label = builder.cashflow_trend_line(1)["datasets"][0]["label"]
        assert label == "Net Cash Flow"

    def test_net_values_are_correct(self, builder):
        data = builder.cashflow_trend_line(1)["datasets"][0]["data"]
        # Jan: 5000 - (1200+300) = 3500
        # Feb: 5000 - (1200+500+200) = 3100
        assert data[0] == pytest.approx(3_500)
        assert data[1] == pytest.approx(3_100)

    def test_data_length_matches_labels(self, builder):
        result = builder.cashflow_trend_line(1)
        assert len(result["labels"]) == len(result["datasets"][0]["data"])



class TestTopExpenseCategoriesBar:

    def test_default_top_n_is_5(self, builder):
        result = builder.top_expense_categories_bar(1)
        assert len(result["labels"]) <= 5

    def test_top_1_returns_one_category(self, builder):
        result = builder.top_expense_categories_bar(1, top_n=1)
        assert len(result["labels"]) == 1

    def test_top_category_is_rent(self, builder):
        # Rent = 2400, Food = 800, Transport = 200
        result = builder.top_expense_categories_bar(1, top_n=1)
        assert result["labels"][0] == "Rent"

    def test_data_is_sorted_descending(self, builder):
        data = builder.top_expense_categories_bar(1, top_n=3)["datasets"][0]["data"]
        assert data == sorted(data, reverse=True)

    def test_invalid_top_n_raises_value_error(self, builder):
        with pytest.raises(ValueError, match="top_n must be at least 1"):
            builder.top_expense_categories_bar(1, top_n=0)

    def test_negative_top_n_raises_value_error(self, builder):
        with pytest.raises(ValueError):
            builder.top_expense_categories_bar(1, top_n=-3)

    def test_dataset_length_matches_labels(self, builder):
        result = builder.top_expense_categories_bar(1, top_n=2)
        assert len(result["labels"]) == len(result["datasets"][0]["data"])



class TestMonthlyTransactionCountBar:

    def test_returns_required_keys(self, builder):
        result = builder.monthly_transaction_count_bar(1)
        assert "labels"   in result
        assert "datasets" in result

    def test_counts_are_positive_integers(self, builder):
        data = builder.monthly_transaction_count_bar(1)["datasets"][0]["data"]
        assert all(isinstance(v, int) and v > 0 for v in data)

    def test_total_count_matches_all_transactions(self, builder):
        data = builder.monthly_transaction_count_bar(1)["datasets"][0]["data"]
        assert sum(data) == 7       # user 1 has 7 rows in sample data

    def test_data_length_matches_labels(self, builder):
        result = builder.monthly_transaction_count_bar(1)
        assert len(result["labels"]) == len(result["datasets"][0]["data"])
