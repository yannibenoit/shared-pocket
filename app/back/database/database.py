from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import logging
import os
from ..api.tools import Tool

tool = Tool()


class MongoDB:

    def __init__(self):
        self.username = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.database_name = os.getenv("DB_NAME")
        self.port = os.getenv("DB_PORT")
        self.client = None

    def connect(self):
        try:
            if self.database_name:
                if self.username and self.password:
                    self.client = MongoClient(f'mongodb://{self.username}:{self.password}@{self.host}:{self.port}/{self.database_name}')
                else:
                    self.client = MongoClient(f'mongodb://{self.host}:{self.port}/{self.database_name}')
            else:
                raise ValueError(f'You must enter a database name')
        except ConnectionFailure as e:
            print(f'Error connecting to MongoDB:{e}')

    def get_collection(self, collection):
        return self.client[self.database_name][collection]

    def insert_element(self, collection, dict_):
        target = self.get_collection(collection)
        result = target.insert(tool.flatten_json_iterative_solution(dict_))
        return result

    def create_unique_index(self, field, collection):
        target = self.get_collection(collection)
        result = target.create_index([(field, 1)], unique=True)
        return result

    def delete_all_documents(self, collection):
        target = self.get_collection(collection)
        result = target.remove({})
        return result

    def get_documents(self, collection, filter_input=dict(), unique=False, fields=None):

        collection = self.get_collection(collection)
        if unique:
            return collection.find_one(filter_input, fields)
        else:
            data = list(collection.find(filter_input, fields))
            return data

    def close(self):
        self.client.close()
