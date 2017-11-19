import dataset

# 対象のDBを指定
DBMS = 'mysql'
USER = 'wsl'
PASS = 'tomohi6'
HOST = 'db02.wsl.mind.meiji.ac.jp'
DB   = 'search_degital_library'
TABLE= 'books'

db = dataset.connect('{0}://{1}:{2}@{3}/{4}'.format(DBMS, USER, PASS, HOST, DB))

from datetime import datetime  as dt
"""
table = db[TABLE]
with open('../src/ver1/PDF_list.txt') as f:
    for line in f:
        if line[:-1] == 'リーダブルコード': continue
        da = dt.now()
        d = '{}-{}-{} {}:{}:{}'.format(da.year, da.month, da.day, da.hour, da.minute, da.second)
        data = dict(name=line[:-1], created=d, modified=d)
        table.insert(data)
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
