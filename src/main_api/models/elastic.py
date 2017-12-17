from elasticsearch import Elasticsearch
import json

class elasticsearch:
    def __init__(self):
        self.__es = Elasticsearch('http://dryer:9200')

    def return_match_records(self, doc_type_, query_match_, index_='search_degital_library'):
        return self.__es.search(index=index_, doc_type=doc_type_, body={"query": {"match": query_match_}, "size": 200, "sort": [{"name": {"order": "desc"}}]})['hits']['hits']

    def return_all_records(self, doc_type_, index_='search_degital_library'):
        return  self.__es.search(index=index_, doc_type=doc_type_, body={"query": {"match_all": {}}, "size": 200, "sort": [{"created": {"order": "desc"}}]})['hits']['hits']

    def return_record(self, doc_type_, id_, index_='search_degital_library'):
        return self.__es.get_source(index=index_, doc_type="categories", id=id_)

    def add_record(self, doc_type_, id_, body_):
        self.__es.index(index="search_degital_library", doc_type=doc_type_, id=id_, body=body_)

    def delete_record(self, doc_type_, id_):
        self.__es.delete(index="search_degital_library", doc_type=doc_type_, id=id_)
