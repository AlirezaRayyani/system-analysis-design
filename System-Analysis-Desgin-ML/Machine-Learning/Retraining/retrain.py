import pandas as pd
from base_user import BaseUserData

class RetrainManager(BaseUserData):

    def should_retrain(self, user_id):
        pass

    def has_new_transactions(self, user_id):
        pass

    def schedule_retrain(self, user_id):
        pass

    def execute_retrain(self, user_id):
        pass

