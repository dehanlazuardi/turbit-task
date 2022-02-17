import string
from django.shortcuts import render
from django.http import JsonResponse
from bson.json_util import dumps

from datetime import datetime
import time
from urllib.parse import quote_plus
import pymongo


def connect_to_mongodb(username: string, password: string, host: string):
    """
        connect to mongodb in the host with
        given username and client, return client pymongo object
    """
    # for username and passwords reserved characters like ‘:’, ‘/’, ‘+’ and ‘@’ must be percent encoded following RFC 2396.
    uri = f"mongodb://{quote_plus(username)}:{quote_plus(password)}@{host}"
    client = pymongo.MongoClient(uri)
    return client

def map_result(item, key):
    modified_item = {}
    modified_item["x"] = item["Dat/Zeit"].isoformat()
    if "value" in item[key].keys():
        modified_item["y"] = item[key]["value"]
    else:
        modified_item["y"] = item[key]
    return modified_item

def index(request):
    return render(request, 'data_display/index.html')

def get_data(request):
    # connect to mongodb, select db and collection
    client = connect_to_mongodb("root", "test1234", "localhost:27017")
    db = client["development"]
    collection = db["turbine-1"]

    # make mongo query
    start_date = datetime(2016, 1, 1, 0, 0, 0)
    end_date = datetime(2016, 3, 1, 23, 59, 0)
    key = "Strom-"
    query = {"Dat/Zeit": {"$gte": start_date, "$lte": end_date}}
    projection = {"_id": 0, key: 1, "Dat/Zeit": 1}
    
    # get data from db
    data = collection.find(query, projection)

    # map to chart.js scatter plot data
    data = [map_result(item, key) for item in data]
    
    return JsonResponse(data, safe=False)