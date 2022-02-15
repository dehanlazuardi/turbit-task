import argparse
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--file-path', '-f', type=str, help='Path to the csv file')
args = parser.parse_args()

def audit_null(df):
    """
        check value in each row for each column 
        is null using built in pandas isnull function.
    """
    #  delete white space, replace with nan
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    df = df.replace("", np.nan)

    print("----Checking Null Value----")
    print("null in column:")
    columns = list(df.columns)
    null_per_col = df.isnull().sum()
    for col in columns:
        print(f" - \"{col}\"\t: {null_per_col[col]}")

    total_null = null_per_col.sum()
    print(f"\ntotal null value: {total_null}")
    ratio = total_null/(df.shape[0]*df.shape[1])*100
    print(f"ratio null/total: {round(ratio,3)}%\n\n")

def audit_numeric(df):
    """
        check value in each row for each column 
        wether numeric or non-numeric 
        using built in pandas is_numeric function.
    """
    print("----Checking Numeric Value----")
    columns = list(df.columns)
    sum_numeric_count = 0
    sum_non_numeric_count = 0
    for col in columns:
        numeric_series = df[col].astype(str).str.isnumeric()
        print(f"column \"{col}\":")

        numeric_count = 0
        if True in set(numeric_series):
            numeric_count = numeric_series.value_counts()[True]
        print(f" - Numeric\t: {numeric_count}")

        non_numeric_count = 0
        if False in set(numeric_series):
            non_numeric_count = numeric_series.value_counts()[False]
        print(f" - Non-numeric\t: {non_numeric_count}\n")

        sum_numeric_count += numeric_count
        sum_non_numeric_count += non_numeric_count

    print(f"total numeric items\t: {sum_numeric_count}")
    print(f"total non-numeric items\t: {sum_non_numeric_count}")
    ratio = sum_non_numeric_count/(sum_numeric_count+sum_non_numeric_count)*100
    print(f"ratio non-numeric/total\t: {round(ratio, 2)}%\n\n")

def audit(df):
    audit_numeric(df)
    audit_null(df)

if __name__ == '__main__':
    # read csv file
    file_path = args.file_path
    print(f"Auditing {file_path} file...\n")
    df = pd.read_csv(file_path, sep=";", decimal=",")

    print(f"shape of df: {df.shape}\n")
    audit(df)



