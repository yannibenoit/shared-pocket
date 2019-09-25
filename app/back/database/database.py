from pymongo import MongoClient
from pathlib import Path
from dotenv import load_dotenv
import os
from ..api.tools import Tool


DB_NAME = os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

tool = Tool()


class MongoDB:

    def __init__(self):
        self.username = DB_USERNAME
        self.password = DB_PASSWORD
        self.host = DB_HOST
        self.name = DB_NAME
        self.port = DB_PORT
        self.client = MongoClient(f'mongodb://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}')
        #self.client = MongoClient(f'mongodb://{self.host}:{self.port}/{self.name}')

    def insert(self, collection, dict_):
        target = self.client[self.name][collection]
        result = target.insert(tool.flatten_json_iterative_solution(dict_))
        return result

    def create_index(self, field, collection):
        target = self.client[self.name][collection]
        result = target.create_index([(field, 1)],unique=True)

    def delete_all_documents(self, collection):
        target = self.client[self.name][collection]
        result = target.remove({})
