import collections
from typing import Collection
import unittest
from .. import load
from dotenv import load_dotenv
import os
import csv
from datetime import datetime


test_file = "test.csv"
rows = [
    ["Dat/Zeit", "col_a", "col_a unit", "col_b"],
    ["01.01.2016, 00:10", "1,3", "unit", "1,3"]
]

load_dotenv()
username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")
host = "localhost:27017"
db_name = "test"
collection_name = "test"

class LoadTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(test_file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            writer.writerows(rows)

    @classmethod
    def tearDownClass(cls):
        # delete test database
        client = load.connect_to_mongodb(username, password, host)
        client.drop_database(db_name)

        # delete test file
        os.remove(test_file)

    def test_connect_to_mongodb(self):
        client = load.connect_to_mongodb(username, password, host)
        self.assertEqual({'ok': 1.0}, client.development.command("ping"))

    def test_csv_to_dict(self):
        data = [{
            "Dat/Zeit": '01.01.2016, 00:10', 
            "col_a": 1.3,
            "col_a unit": "unit",
            "col_b": 1.3
        }]
        record = load.csv_to_dict(test_file)

        self.assertEqual(data, record)

    def test_arrange_dict(self):
        data = [{
            "Dat/Zeit": datetime.strptime("01.01.2016, 00:10", "%d.%m.%Y, %H:%M"), 
            "col_a": {
                "value": 1.3,
                "unit": "unit"
            },  
            "col_b": 1.3
        }]

        record = load.csv_to_dict(test_file)
        arranged = load.arrange_dict(record)

        self.assertEqual(data, arranged)
        
    
    def test_load_to_db(self):
        data = {
            "Dat/Zeit": datetime.strptime("01.01.2016, 00:10", "%d.%m.%Y, %H:%M"), 
            "col_a": {
                "value": 1.3,
                "unit": "unit"
            },  
            "col_b": 1.3
        }
        
        # load data to db
        load.load_to_db(username, 
            password, 
            host,
            db_name,
            collection_name,
            test_file)

        #  connect to db
        client = load.connect_to_mongodb(username, password, host)
        db = client[db_name]
        collections = db[collection_name]
        
        # get item from db
        item = collections.find_one()
        
        # delete _id
        del item["_id"]

        self.assertEqual(data, item)



