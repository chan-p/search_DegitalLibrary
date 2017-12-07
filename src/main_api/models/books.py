import dataset
from elasticsearch import Elasticsearch
import os
from . import elastic
from datetime import datetime  as dt


class book:
    def __init__(self, title=None, id_=None):
        self.title = title
        self.id = id_
        self.__path = os.environ.get('DB02_CONNECT')
        self.__es = Elasticsearch("localhost:9200")
        self.__db = dataset.connect(self.__path)
        self.__table_books = self.__db['books']
        self.__table_books_categories = self.__db['books_categories']
        self.__table_categories = self.__db['categories']
        self.__ES = elastic.elasticsearch()

    def get_id(self, flg=False):
        self.id = self.__table_books.find_one(name=self.title)['id']
        if flg: return self.id

    def get_title(self, flg):
        self.title = self.__table_books.find_one(id=self.id)['name']
        if flg: return self.title

    def get_category(self):
        books = []
        categories = [record['_source']['category_id'] for record in  self.__es.search(index="search_degital_library", doc_type="books_categories", body={"query": {"match": {'book_id': self.id}}, "size": 200, "sort": [{"name": {"order": "desc"}}]})['hits']['hits']]
        return [self.__ES.return_record("categories", id_)['name'] for id_ in categories]

    def get_categories(self):
        books = {}
        categories = {}
        for record in self.__ES.return_all_records("categories"):
            categories[int(record['_id'])] = record['_source']['name']
        for record in self.__ES.return_all_records("books_categories"):
            if record['_source']['book_id'] not in books:
                books[record['_source']['book_id']] = []
            books[record['_source']['book_id']].append(categories[record['_source']['category_id']])
        return books

    def get_ids_date(self, date):
        day = int(date.split('-')[2]) + 1
        if int(day) < 10:
            day = '0' + str(day)
        month = str(int(date.split('-')[1]))
        if int(day) > 31:
            day = '01'
            month = str(int(date.split('-')[1]) + 1)
        next_day = '{0}-{1}-{2}'.format(date.split('-')[0], month, day)
        print("SELECT * FROM books where created between "+str(date)+" and "+str(next_day))
        result = self.__db.query("SELECT * FROM books where created between '"+str(date)+"' and '"+str(next_day)+"'")
        return [(book['id'], book['name']) for book in result]

    def get_all_ids(self):
        return [(pdf['_id'], pdf['_source']['name'], pdf['_source']['created']) for pdf in self.__ES.return_all_records("books")]

    def search_ids(self, word):
        title_list = []
        result = self.__db.query("SELECT id FROM books where name like '%"+word+"%'")
        for record in result:
            title_list.append(record['id'])
        return title_list

    def add_title(self):
        data = dict(name=self.title, created=self.__return_date(), modified=self.__return_date())
        self.__table_books.insert(data)
        date = self.__table_books.find_one(id=self.get_id(True))["created"]
        self.__ES.add_record("books", self.get_id(True), {"name":self.title, "created":date, "modified":date})

    def add_related_category(self, category_id):
        data = dict(book_id=self.get_id(True), category_id=category_id)
        self.__table_books_categories.insert(data)
        id_ = self.__table_books_categories.find_one(book_id=self.id, category_id=category_id)['id']
        self.__ES.add_record("books_categories", id_, {"book_id":self.id, "category_id":category_id})

    def delete_related_category(self, category_id):
        self.get_id()
        data = dict(book_id=self.id, category_id=category_id)
        id_ = self.__table_books_categories.find_one(book_id=self.id, category_id=category_id)['id']
        self.__table_books_categories.delete(id=id_)
        self.__ES.delete_record(books_categories, id_)

    def __return_date(self):
        da = dt.now()
        return '{}-{}-{} {}:{}:{}'.format(da.year, da.month, da.day, da.hour, da.minute, da.second)
