import dataset

# 対象のDBを指定
DBMS = 'mysql'
USER = 'root'
PASS = 'jvb1l0Iwata'
HOST = 'db02.wsl.mind.meiji.ac.jp'
DB   = 'search_degital_library'
TABLE= 'books'

db = dataset.connect('{0}://{1}:{2}@{3}/{4}'.format(DBMS, USER, PASS, HOST, DB))

from datetime import datetime  as dt


table = db['categories']
table2 = db['books']
table3 = db['books_categories']
with open('../src/main_api/cate_search.txt') as f:
    for line in f:
        # if line[:-1] == 'リーダブルコード': continue
        cate = line[:-1].split(',')
        res = table.find_one(name=cate[0])
        for name in cate[1:]:
            res2 = table2.find_one(name=name)
            data = dict(book_id=res2['id'], category_id=res['id'])
            table3.insert(data)
        """
        da = dt.now()
        d = '{}-{}-{} {}:{}:{}'.format(da.year, da.month, da.day, da.hour, da.minute, da.second)
        """

"""
table = db[TABLE]
table2 = db['categories']
da = dt.now()
d = '{}-{}-{} {}:{}:{}'.format(da.year, da.month, da.day, da.hour, da.minute, da.second)
with open('../src/ver1/cate_search.txt') as f:
    for line in f:
        cate = line[:-1].split(',')[0]
        book_list = line[:-1].split(',')[1:]
        for name in book_list:
            data = dict(name=cate, book_id=table.find_one(name=name)['id'], created=d, modified=d)
            table2.insert(data)
"""
