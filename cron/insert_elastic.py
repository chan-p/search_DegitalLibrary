import dataset
from elasticsearch import Elasticsearch
es = Elasticsearch("localhost:9200")

DBMS = 'mysql'
USER = 'root'
PASS = 'jvb1l0Iwata'
HOST = 'db02.wsl.mind.meiji.ac.jp'
DB   = 'search_degital_library'
TABLE= 'books'

db = dataset.connect('{0}://{1}:{2}@{3}/{4}?charset=utf8'.format(DBMS, USER, PASS, HOST, DB))

table_books = db['books']

for data in table_books.find():
    es.index(index="search_degital_library", doc_type="books", id=data['id'], body={"name":data['name'], "created":data['created'], "modified":data['modified']})

table_categories = db['categories']

for data in table_categories.find():
    es.index(index="search_degital_library", doc_type="categories", id=data['id'], body={"name":data['name'], "created":data['created'], "modified":data['modified']})


table_books_categories = db['books_categories']

for data in table_books_categories.find():
    es.index(index="search_degital_library", doc_type="books_categories", id=data['id'], body={"book_id":data['book_id'], "category_id":data['category_id']})
