import pymongo
from datetime import datetime
from urllib.parse import quote_plus

class MongoLoader:
    def __init__(self):
        self._dataframe = None

    def connect(self, username, password, host):
        # for username and passwords reserved characters like ‘:’, ‘/’, ‘+’ and ‘@’ must be percent encoded following RFC 2396.
        uri = f"mongodb://{quote_plus(username)}:{quote_plus(password)}@{host}"
        self.client = pymongo.MongoClient(uri)

    def add_data(self, data):
        self._dataframe = data

    def _parse(self):
        """
            convert df to python dictionary

                [{"column_1": df["column_1"][i], ... ,"column_n": df["column_n"][i]},
                ...
                {"column_1": df["column_1"][n], ... ,"column_n": df["column_n"][n]}]

            arrange exported dict from csv_to_dict() to
            db structure in mongo db, return list of dict
        """
        records = self._dataframe.to_dict('records')

        arranged_dict = []
        for item in records:
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
    
    def load(self, db_name, col_name):
        # choose colection
        db = self.client[db_name]
        collection = db[col_name]

        # parse df to mongo data structure
        arranged_dict = self._parse()
        
        # insert to db
        res = collection.insert_many(arranged_dict)

class DBLoaderFactory:
    def __init__(self):
        self._loader = {}

    def register(self, name: str, function):
        self._loader[name] = function

    def get(self, name: str):
        loader = self._loader.get(name)
        if loader == None:
            raise ValueError(name)
        return loader()

db_loader_factory = DBLoaderFactory()
db_loader_factory.register('mongodb', MongoLoader)