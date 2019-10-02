from ..database.database import MongoDB

from ..database.database import MongoDB


class Articles:

    def __init__(self):
        self.username = None
        self.access_token = None
        self.article_collection = "articles"
        self.article_collection_index = "item_id"
        self.db = MongoDB()

    def create_article(self, user_data=dict()):
        self.db.connect()
        self.db.insert_element(self.article_collection, user_data)
        self.db.close()
        return user_data

    def get_articles(self):
        self.db.connect()
        users = self.db.get_documents(self.article_collection)
        self.db.close()
        return users

    def get_article(self, index):
        self.db.connect()
        user = self.db.get_documents(self.article_collection, filter_input={self.article_collection_index: index}, unique=True)
        self.db.close()
        return user

    def create_article_index(self):
        self.db.connect()
        self.db.create_unique_index(self.article_collection_index, self.article_collection)
        self.db.close()

    def update_articles(self, field):
        return field
