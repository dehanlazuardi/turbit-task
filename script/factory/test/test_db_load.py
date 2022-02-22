import pymongo
from datetime import datetime
from urllib.parse import quote_plus
import os
import csv
import unittest
from dotenv import load_dotenv
from .. import db_load
import pandas as pd



test_file = "temp.csv"
rows = [
    ["Dat/Zeit", "col_a", "col_a unit", "col_b"],
    ["01.01.2016, 00:10", "1,3", "unit", "1,3"]
]

load_dotenv()
username = "root"
password = "test1234"
host = "localhost:27017"
db_name = "test"
collection_name = "test"

class DBLoadTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # create temp csv for testing only
        with open(test_file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            writer.writerows(rows)

    @classmethod
    def tearDownClass(cls):
        # delete test database
        uri = f"mongodb://{quote_plus(username)}:{quote_plus(password)}@{host}"
        client = pymongo.MongoClient(uri)
        client.drop_database(db_name)

        # delete test file
        os.remove(test_file)

    def test_MongoLoader_connect(self):
        db_loader = db_load.MongoLoader()
        db_loader.connect(username, password, host)

        self.assertEqual({'ok': 1.0}, db_loader.client.development.command("ping"))


    def test_MongoLoader_load(self):
        data = {
            "Dat/Zeit": datetime.strptime("01.01.2016, 00:10", "%d.%m.%Y, %H:%M"), 
            "col_a": {
                "value": 1.3,
                "unit": "unit"
            },  
            "col_b": 1.3
        }

        df = pd.read_csv(test_file, sep=";", decimal=",")

        # load data to db
        db_loader = db_load.MongoLoader()
        db_loader.connect(username, password, host) 
        db_loader.add_data(df)
        db_loader.load(db_name, collection_name)
        
        # get item from db
        db = db_loader.client[db_name]
        collections = db[collection_name]
        item = collections.find_one()
        
        # delete _id
        del item["_id"]

        self.assertEqual(data, item)