import argparse
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--file-path', '-f', type=str, help='Path to the csv file')
parser.add_argument('--folder-path', '-o', type=str, help='Path to output folder')
args = parser.parse_args()

if __name__ == '__main__':
    # read csv file
    file_path = args.file_path
    print(f"Cleaning {file_path} file...\n")
    df = pd.read_csv(file_path, sep=";", decimal=",")

    # strip white space from column names
    df.columns = df.columns.str.strip()

    # extract unit from first row, make new unit columns
    units = df.iloc[0]
    units = units.str.strip()
    units = units.replace("", np.nan)
    units = units.dropna()
    for col in list(df.columns):
        if col in list(units.index):
            # create column, assign unit to the new columns
            col_unit_name = col+" unit"
            df[col_unit_name] = units[col]
    
    # restart indexed to 0 because we already drop the first index
    df = df.drop([0]).reset_index(drop=True)

    # parse time
    df['Dat/Zeit'] = pd.to_datetime(df['Dat/Zeit'], format="%d.%m.%Y, %H:%M")

    # save to csv
    df.to_csv(args.folder_path, sep=';')