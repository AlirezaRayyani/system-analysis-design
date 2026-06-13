import pandas as pd


class BaseUserData:
    """
    Shared base class for StatisticalAnalysis and ChartDataBuilder.
    Centralizes common data access and preparation logic (DRY principle).
    """

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe

    def _for_user(self, user_id: int | str) -> pd.DataFrame:
        """
        Return raw transactions for a specific user.
        """
        return self.df[self.df["User ID"] == user_id].copy()

    def _prepare_user_data(self, user_id: int | str) -> pd.DataFrame:
        """
        Returns a DataFrame with 'Date Time' parsed as timezone-naive datetime.
        """
        data = self._for_user(user_id)
        data["Date Time"] = pd.to_datetime(data["Date Time"]).dt.tz_localize(None)
        return data