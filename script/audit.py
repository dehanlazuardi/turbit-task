import argparse
import pandas as pd

file_path = "./data/raw/Turbine1.csv"

parser = argparse.ArgumentParser()
parser.add_argument('--file-path', '-f', type=str, help='Path to the csv file')
args = parser.parse_args()

if __name__ == '__main__':
    print(f"checking {args.file_path} file\n")
    df = pd.read_csv(file_path, sep=";")
    print(df.head())
    
    # df shape 
    print(f"\n1. shape of the df: {df.shape}")

    # data types
    print("\n2. data types in each columns:")
    print(df.dtypes)

    # count missing value
    print("\n3. missing value in each columns:")
    null_per_col = df.isnull().sum()
    print(null_per_col)

    # summary
    print("\nSummary:")
    total_data = df.shape[0]*df.shape[1]
    print(f" - total data: {total_data}")
    total_null = null_per_col.sum()
    print(f" - total null value: {total_null}")
    ratio = total_null/total_data * 100
    print(f" - null value ratio: {ratio}%")



