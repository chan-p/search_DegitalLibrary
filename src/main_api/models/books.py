import dataset
import os


class book:
    def __init__(self, title):
        self.title = title


class books:
    def __init__(self):
        self.path = os.environ.get('DB02_CONNECT')
        self.db = dataset.connect(self.path)
        self.table_books = self.db['books']

    def get_all_title(self):
        PDF_list = self.table_books.find()
        list_ = []
        for pdf in PDF_list:
            list_.append(pdf['name'])
        return list_
