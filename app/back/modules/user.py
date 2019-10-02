from ..database.database import MongoDB


class User:

    def __init__(self):
        self.username = None
        self.access_token = None
        self.user_collection = "users"
        self.user_collection_index = "username"
        self.db = MongoDB()

    def create_user(self, user_data=dict()):
        self.db.connect()
        self.db.insert_element(self.user_collection, user_data)
        self.db.close()
        return user_data

    def get_users(self):
        self.db.connect()
        users = self.db.get_documents(self.user_collection)
        self.db.close()
        return users

    def get_user(self, index):
        self.db.connect()
        user = self.db.get_documents(self.user_collection, filter_input={self.user_collection_index: index}, unique=True)
        self.db.close()
        return user

    def create_user_index(self):
        self.db.connect()
        self.db.create_unique_index(self.user_collection_index, self.user_collection)
        self.db.close()

    def update_user(self, field):
        return field
