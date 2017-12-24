import dataset
from elasticsearch import Elasticsearch
es = Elasticsearch("elasticsearch:9200")

DBMS = 'mysql'
USER = 'spark'
PASS = 'wsl-slave'
HOST = 'db'
DB = 'search_degital_library'
TABLE = 'books'

db_info = '{0}://{1}:{2}@{3}/{4}?charset=utf8'.format(
    DBMS, USER, PASS, HOST, DB)

print("connect → {}".format(db_info))
db = dataset.connect(db_info)

table_books = db['books']

for data in table_books.find():
    es.index(index="search_degital_library", doc_type="books", id=data['id'], body={
             "name": data['name'], "created": data['created'], "modified": data['modified']})

table_categories = db['categories']

for data in table_categories.find():
    es.index(index="search_degital_library", doc_type="categories", id=data['id'], body={
             "name": data['name'], "created": data['created'], "modified": data['modified']})


table_books_categories = db['books_categories']

for data in table_books_categories.find():
    es.index(index="search_degital_library", doc_type="books_categories", id=data[
             'id'], body={"book_id": data['book_id'], "category_id": data['category_id']})

print("insert done")
