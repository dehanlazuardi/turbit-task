import string
import pandas as pd
import pymongo
import argparse
from datetime import datetime
from urllib.parse import quote_plus


parser = argparse.ArgumentParser()
parser.add_argument('--file-path', '-f', type=str, help='Path to the csv file')
parser.add_argument('--username', '-u', type=str, help='Mongo db username')
parser.add_argument('--password', '-p', type=str, help='Mongo db password')
parser.add_argument('--host', '-a', type=str, help='Mongo db host')
parser.add_argument('--database-name', '-d', type=str, help='Mongo db database name')
parser.add_argument('--collection-name', '-c', type=str, help='collection name of the database')
args = parser.parse_args()

def connect_to_mongodb(username: string, password: string, host: string):
    """
        connect to mongodb in the host with
        given username and client, return client pymongo object
    """
    # for username and passwords reserved characters like ‘:’, ‘/’, ‘+’ and ‘@’ must be percent encoded following RFC 2396.
    uri = f"mongodb://{quote_plus(username)}:{quote_plus(password)}@{host}"
    client = pymongo.MongoClient(uri)
    return client

def csv_to_dict(file_path: string) -> dict:
    """
        convert csv to python dictionary
        return dictionary with
            [{"column_1": df["column_1"][i], ... ,"column_n": df["column_n"][i]},
            ...
            {"column_1": df["column_1"][n], ... ,"column_n": df["column_n"][n]}]

    """
    df = pd.read_csv(file_path, sep=";", decimal=",")
    return df.to_dict('records')

def arrange_dict(records_dict: dict) -> list:
    """
        arrange exported dict from csv_to_dict() to
        db structure in mongo db, return list of dict
    """
    arranged_dict = []
    for item in records_dict:
        # parse datetime
        item["Dat/Zeit"] = datetime.strptime(item["Dat/Zeit"], "%d.%m.%Y, %H:%M")
        
        # group unit with its value
        col_unit_names = []
        for key in item.keys():
            if "unit" in key:
                col_name, _ = key.split(" unit")

                # group unit and value
                item[col_name] = {
                    "value": item[col_name],
                    "unit": item[key]
                }

                # delete unit dict
                col_unit_names.append(key)
        
        # delete unit from dict
        for col_name in col_unit_names:
            del item[col_name]

        arranged_dict.append(item)

    return arranged_dict

def load_to_db(username: string, password: string, host: string, 
            database_name: string, collection_name: string, file_path: string):
    """
        load csv to dataframe
        parse dataframe to desired dict/json format
        insert to mongodb
    """
    # connect and choose collection
    client = connect_to_mongodb(username, password, host)
    db = client[database_name]
    collection = db[collection_name]

    # load and parse csv
    records_dict = csv_to_dict(file_path)
    arranged_dict = arrange_dict(records_dict)

    # insert to db
    collection.insert_many(arranged_dict)
    
if __name__ == '__main__':
    load_to_db(args.username, args.password, args.host,
                args.database_name, args.collection_name, args.file_path)
    