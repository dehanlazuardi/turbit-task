import string
from django.shortcuts import render
from django.http import JsonResponse
import os

from datetime import datetime
import time
from urllib.parse import quote_plus
import pymongo

# get db cred
db_username= os.environ['DB_USERNAME']
db_password= os.environ['DB_PASSWORD']
db_host= os.environ['DB_HOST']


def connect_to_mongodb(username: string, password: string, host: string):
    """
        connect to mongodb in the host with
        given username and client, return client pymongo object
    """
    # for username and passwords reserved characters like ‘:’, ‘/’, ‘+’ and ‘@’ must be percent encoded following RFC 2396.
    uri = f"mongodb://{quote_plus(username)}:{quote_plus(password)}@{host}"
    client = pymongo.MongoClient(uri)
    return client

def make_mongo_query(start: string, end: string, key: string):
    """
        make mongodb query
    """
    start_date = datetime.strptime(start, '%Y-%m-%dT%H:%M')
    end_date = datetime.strptime(end, '%Y-%m-%dT%H:%M')
    query = {"Dat/Zeit": {"$gte": start_date, "$lte": end_date}}
    projection = {"_id": 0, key: 1, "Dat/Zeit": 1}
    return (query, projection)

def map_result(item, key):
    """
        convert mongodb dict to FE format
    """
    value = 0
    if "value" in item[key].keys():
        value = item[key]["value"]
    else:
        value = item[key]
    posix_time = time.mktime(item["Dat/Zeit"].timetuple()) * 1000
    return [posix_time, value]

def index(request):
    return render(request, 'data_display/index.html')

def get_data(request):
    # connect to mongodb, select db and collection
    client = connect_to_mongodb(db_username, db_password, db_host)
    db = client["development"]
    collection = db["turbine-1"]
    if request.GET["turbine"] == '2' :
        collection = db["turbine-2"]
    
    # make mongo query
    key = request.GET["key"]
    query, projection = make_mongo_query(request.GET["start"], request.GET["end"], key)
    
    # get data from db
    data = collection.find(query, projection)

    # get data's unit from db
    unit = collection.find_one(projection={"_id": 0, key+".unit": 1, })

    # build response
    mapped_data = [map_result(item, key) for item in data]
    resp = {
        "data": mapped_data,
        "unit": unit[key]["unit"]
    }

    return JsonResponse(resp, safe=False)