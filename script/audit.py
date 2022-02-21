import argparse
import pandas as pd
import numpy as np
from factory.null_auditor import NullAuditor

parser = argparse.ArgumentParser()
parser.add_argument('--file-path', '-f', type=str, help='Path to the csv file')
args = parser.parse_args()

def audit_null(df):
    """
        check value in each row for each column is null.
    """
    # audit null
    null_auditor = NullAuditor()
    null_per_col = null_auditor.audit(df, "pd_null")

    #  print result
    print("----Checking Null Value----")
    print("null in column:")
    for key in null_per_col.keys():
        print(f" - \"{key}\"\t: {null_per_col[key]}")

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
    sum_digit_count = 0
    sum_non_digit_count = 0
    for col in columns:
        print(f"column \"{col}\":")
        # delete "." and "-", otherwise for real number 0.3 and minus -9 wont be recognized as digit
        stripped = df[col].astype(str).str.replace(".", "", 1, regex=False).str.lstrip('-')
        digit_series = stripped.str.isdigit()

        numeric_count = 0
        if True in set(digit_series):
            numeric_count = digit_series.value_counts()[True]
        print(f" - digit\t: {numeric_count}")

        non_numeric_count = 0
        if False in set(digit_series):
            non_numeric_count = digit_series.value_counts()[False]
        print(f" - non-digit\t: {non_numeric_count}\n")

        sum_digit_count += numeric_count
        sum_non_digit_count += non_numeric_count

    print(f"total digit items\t: {sum_digit_count}")
    print(f"total non-digit items\t: {sum_non_digit_count}")
    ratio = sum_non_digit_count/(sum_digit_count+sum_non_digit_count)*100
    print(f"ratio non-digit/total\t: {round(ratio, 2)}%\n\n")

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



