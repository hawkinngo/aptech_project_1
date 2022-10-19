import pandas as pd


def df_read_csv(csv_file_path):
    df_csv = pd.read_csv(csv_file_path)
    first_column = df_csv.columns[0]
    df_csv = df_csv.drop([first_column], axis=1)
    return df_csv
