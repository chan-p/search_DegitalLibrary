
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import numpy as np
import codecs

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)

# ここからウェブアプリケーション用のルーティングを記述
# index にアクセスしたときの処理
@app.route('/', methods=['GET'])
def index():
    title = request.args.get('title').encode('utf-8').decode('utf-8')
    print(type(title))
    column = request.args.get('column')
    line = []
    flg = 0
    with codecs.open('./PDF_list_column.txt', 'r', 'utf-8') as f:
        for li in f:
            lis = li[:-1].split(',')
            rr = li[:-1]
            if title == lis[0]:
                print('OK')
                rr += ',' + column
            line.append(rr + '\n')
    with codecs.open('./PDF_list_column.txt', 'w', 'utf-8') as g:
        for jj in line:
            g.write(jj)
    response = make_response()
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/delete/', methods=['GET'])
def index1():
    title = request.args.get('title').encode('utf-8').decode('utf-8')
    print(type(title))
    column = request.args.get('column')
    line = []
    flg = 0
    with codecs.open('./PDF_list_column.txt', 'r', 'utf-8') as f:
        for li in f:
            lis = li[:-1].split(',')
            rr = li[:-1]
            if title == lis[0]:
                print('OK')
                print(lis)
                lis.remove(column)
                print(lis)
            line.append(",".join(lis) + '\n')
    with codecs.open('./PDF_list_column.txt', 'w', 'utf-8') as g:
        for jj in line:
            print(jj)
            g.write(jj)
    response = make_response()
    response.headers["Content-Type"] = "application/json"
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0') # どこからでもアクセス可能に
