import argparse
import pandas as pd
import numpy as np
from factory.null_auditor import NullAuditor
from factory.numeric_auditor import NumericAuditor

parser = argparse.ArgumentParser()
parser.add_argument('--file-path', '-f', type=str, help='Path to the csv file')
args = parser.parse_args()

def audit_null(df):
    """
        check whether value in each row is null.
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
        check whether value in each row is non-numeric.
    """
    
    #  audit numeric
    numeric_auditor = NumericAuditor()
    non_numeric_per_column = numeric_auditor.audit(df, 'pd_numeric')

    #  print result
    print("----Checking Numeric Value----")
    print("non-numeric in column:")
    for key in non_numeric_per_column.keys():
        print(f" - \"{key}\"\t: {non_numeric_per_column[key]}")

    total_non_numeric = non_numeric_per_column.sum()
    print(f"\ntotal non-numeric value: {total_non_numeric}")
    ratio = total_non_numeric/(df.shape[0]*df.shape[1])*100
    print(f"ratio non-numeric/total: {round(ratio,3)}%\n\n")

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



