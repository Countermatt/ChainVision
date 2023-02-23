import pandas as pd
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
df = pd.read_csv(dir_path + "/../../data/processed_data/account/account_list.csv", usecols=['account']).drop_duplicates(keep='first').reset_index()
file_name =dir_path + "/../../data/processed_data/account/account_list_unique.csv"
df.to_csv(file_name, index=False)