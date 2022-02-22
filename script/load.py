import string
import pandas as pd
import pymongo
import argparse
from datetime import datetime
from urllib.parse import quote_plus
from factory.db_loader import DBLoader


parser = argparse.ArgumentParser()
parser.add_argument('--file-path', '-f', type=str, help='Path to the csv file')
parser.add_argument('--username', '-u', type=str, help='Mongo db username')
parser.add_argument('--password', '-p', type=str, help='Mongo db password')
parser.add_argument('--host', '-a', type=str, help='Mongo db host')
parser.add_argument('--database-name', '-d', type=str, help='Mongo db database name')
parser.add_argument('--collection-name', '-c', type=str, help='collection name of the database')
args = parser.parse_args()

def load_to_db(username: string, password: string, host: string, 
            database_name: string, collection_name: string, file_path: string):
    """
        load csv to dataframe
        parse dataframe to desired dict/json format
        insert to mongodb
    """
    db_loader = DBLoader()

    df = pd.read_csv(file_path, sep=";", decimal=",")
    db_loader.load(username, password, host, 
                database_name, collection_name, df, 'mongodb')
    
if __name__ == '__main__':
    load_to_db(args.username, args.password, args.host,
                args.database_name, args.collection_name, args.file_path)
    