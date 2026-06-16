import pandas as pd
from base_user import BaseUserData


class TrainingModel(BaseUserData):
    def __init__(self, user_id):
        self.user_id = user_id


    def predict_date(self):
        pass

    def predict_next_7_days(self):
        pass

    def predict_total_week_net_flow(self):
        pass
    