import dataset
from datetime import datetime  as dt
from elasticsearch import Elasticsearch
import os


class category:
    def __init__(self, name=None):
        self.id = None
        self.name = name
        self.__path = os.environ.get('DB02_CONNECT')
        self.__db = dataset.connect(self.__path)
        self.__es = Elasticsearch("localhost:9200")
        self.__table_categories = self.__db['categories']
        self.__table_books_categories = self.__db['books_categories']

    def get_id(self, flg=False):
        if self.__db.query("SELECT count(*) FROM categories WHERE name='" + self.name+"'").next()['count(*)'] == 0:
            self.id = 'no_id'
        else:
            self.id = self.__table_categories.find_one(name=self.name)['id']
        if flg: return self.id

    def add_id(self):
        da = dt.now()
        date = '{}-{}-{}T{}:{}:{}'.format(da.year, da.month, da.day, da.hour, da.minute, da.second)
        data = dict(name=self.name, created=date, modified=date)
        self.__table_categories.insert(data)
        id_ = self.get_id(True)
        self.__es.index(index="search_degital_library", doc_type="categories", id=str(id_), body={"name":self.name, "created":date, "modified":date})

    def get_book_ids(self):
        ids = []
        books = self.__table_books_categories.find(category_id=self.get_id(True))
        for book in books:
            ids.append(book['book_id'])
        return ids

    def get_all_name(self):
        categories = self.__table_categories.find()
        list_ = []
        for category in categories:
            list_.append(category['name'])
        return list_
