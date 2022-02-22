from .db_load import db_loader_factory

class DBLoader:
    def load(self, username, password, host, db_name, col_name, data, name: str):
        db_loader = db_loader_factory.get(name)
        db_loader.connect(username, password, host) 
        db_loader.add_data(data)
        db_loader.load(db_name, col_name)
