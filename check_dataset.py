
import pandas as pd
import os

file_path = "data/raw/online_retail_II.xlsx"

if not os.path.exists(file_path):
    print("Dataset not found!")
else:
    df = pd.read_csv(file_path, sep="\t", nrows=1000)

    print("Dataset loaded successfully!")
    print("Rows loaded for initial inspection:", len(df))
    print("Columns:", df.columns.tolist())

    print("\nFirst 5 records:")
    print(df.head())

    print("\nData types:")
    print(df.dtypes)
