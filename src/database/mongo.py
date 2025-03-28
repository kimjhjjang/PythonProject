from pymongo import MongoClient
from src.util import read_config_yaml


class Mongo(object):

    client = None
    database = None

    def __init__(self):

        config = read_config_yaml()
        uri = config.get('mongo.uri')
        if uri is None:
            raise ValueError('mongo uri not configured')

        if self.client is None:
            client = MongoClient(uri)
            if client is None:
                raise ValueError('MongoClient is None')
            self.client = client


    def set_database(self, database):
        self.database = self.client.get_database(database)


    def create_collection(self, collection):
        if collection not in self.database.list_collection_names():
            res = self.database.create_collection(collection)
            print(res)


    def drop_collection(self, collection):
        if collection not in self.database.list_collection_names():
            self.database.drop_colleciton(collection)


    def insert(self, collection, data):
        if collection not in self.database.list_collection_names():
            return 0

        if isinstance(data, dict):
            res = self.database[collection].insert_one(data)
            if res.acknowledged:
                return 1
            else:
                return 0
        elif isinstance(data, list):
            res = self.database[collection].insert_many(data)
            if res.acknowledged:
                return len(res.inserted_ids)
            return 0
