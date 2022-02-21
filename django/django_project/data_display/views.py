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
# db_username="root"
# db_password="test1234"
# db_host="localhost:27017"

def _connect_to_mongodb(username: string, password: string, host: string):
    """
        connect to mongodb in the host with
        given username and client, return client pymongo object
    """
    # for username and passwords reserved characters like ‘:’, ‘/’, ‘+’ and ‘@’ must be percent encoded following RFC 2396.
    uri = f"mongodb://{quote_plus(username)}:{quote_plus(password)}@{host}"
    client = pymongo.MongoClient(uri)
    return client

def _make_data_query(start: string, end: string, keys: list):
    """
        make mongodb query for getting data
    """
    start_date = datetime.strptime(start, '%Y-%m-%dT%H:%M')
    end_date = datetime.strptime(end, '%Y-%m-%dT%H:%M')
    
    # make query
    query = {"Dat/Zeit": {"$gte": start_date, "$lte": end_date}}

    # make projection
    projection = {"_id": 0}
    for key in keys:
            projection[key] = {
                "$ifNull": [ f"${key}.value", f"${key}", "" ]
            }
    return (query, projection)

def _make_unit_query(keys: list):
    """
        make mongodb query for getting unit
    """
    # make projection
    unit_projection = {"_id": 0}
    for key in keys:
        unit_projection[key] = {
           "$ifNull": [ f"${key}.unit", "" ]
        }
    return unit_projection


def _map_result(item, keys):
    """
        convert mongodb dict to FE format
    """
    res = []
    for key in keys:
        if key == "Dat/Zeit":
            posix_time = time.mktime(item[key].timetuple()) * 1000
            res.append(posix_time)
        else:
            res.append(item[key])
    return res

def index(request):
    return render(request, 'data_display/index.html')

def get_data(request):
    # connect to mongodb, select db and collection
    client = _connect_to_mongodb(db_username, db_password, db_host)
    db = client["development"]
    collection_name = f"turbine-{request.GET['turbine']}"
    collection = db[collection_name]
    
    # make mongo query
    keys = request.GET.getlist("key")
    query, projection = _make_data_query(request.GET["start"], request.GET["end"], keys)
    
    # check is data empty
    if collection.count_documents(query) == 0:
        resp = {
            "data": [],
            "unit": [],
            "name": [],
        }
        return JsonResponse(resp, safe=False)

    # get data from db
    data = collection.find(query, projection)

    # get data's unit from db
    unit_projection = _make_unit_query(keys)
    units = collection.find_one(projection=unit_projection)

    # build response
    mapped_data = [_map_result(item, keys) for item in data]
    mapped_unit = [units[key] for key in keys]
    resp = {
        "data": mapped_data,
        "unit": mapped_unit,
        "name": keys
    }

    return JsonResponse(resp, safe=False)