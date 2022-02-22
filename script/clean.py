import argparse
import pandas as pd
import numpy as np
from factory.data_cleaner import DataCleaner

parser = argparse.ArgumentParser()
parser.add_argument('--file-path', '-f', type=str, help='Path to the csv file')
parser.add_argument('--folder-path', '-o', type=str, help='Path to output folder')
args = parser.parse_args()

if __name__ == '__main__':
    # read csv file
    file_path = args.file_path
    print(f"Cleaning {file_path} file...\n")
    df = pd.read_csv(file_path, sep=";", decimal=",")

    #  clean data
    data_cleaner = DataCleaner()
    df = data_cleaner.clean(df, 'pd_cleaner')

    # save to csv
    df.to_csv(args.folder_path, sep=';', index=False)