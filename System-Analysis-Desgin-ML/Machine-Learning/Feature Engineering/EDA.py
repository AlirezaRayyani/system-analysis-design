import pandas as pd
import datetime
import numpy as np
from base_user import BaseUserData

class FeatureExtractor(BaseUserData):
    def __init__(self, user_id):
        self.user_id = user_id

    def extract_income_features(self):
        pass


    def extract_expense_features(self):
        pass


    def build_training_dataset(self):
        pass


    def calculate_daily_net_flow(self):
        pass
