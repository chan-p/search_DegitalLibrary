from flask import Flask, request, jsonify, make_response
from models import books, categories
import codecs
import json
import configparser
import dataset
import requests

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('./setting.ini')
ENV = config.items('LOCALTEST')

@app.route('/addcate/', methods=['GET'])
def add_category():
    title = request.args.get('title').encode('utf-8').decode('utf-8')
    category_name = request.args.get('column')
    target_category = categories.category(category_name)
    if target_category.get_id(True) == 'no_id':
        target_category.add_id()
    books.book(title).add_related_category(target_category.id)
    return _make_response()

@app.route('/deletecate/', methods=['GET'])
def delete_cate():
    book_title = request.args.get('title').encode('utf-8').decode('utf-8')
    category_name = request.args.get('column')
    target_category = categories.category(category_name)
    books.book(book_title).delete_related_category(target_category.get_id(True))
    return _make_response()

@app.route('/searchcate/', methods=['GET'])
def search_cate():
    book_titles = {}
    category_name = request.args.get('column')
    book_ids = categories.category(category_name).get_book_ids()
    for id_ in book_ids:
        target_book = books.book(id_=id_)
        book_titles[target_book.get_title(True)] = target_book.get_category()
    return _make_response(json.dumps({
                'titles': book_titles
            }))

@app.route('/searchdate/', methods=['GET'])
def search_date():
    book_titles = {}
    date = request.args.get('date')
    book_ids = books.book().get_ids_date(date)
    for id_ in book_ids:
        target_book = books.book(id_=id_[0])
        book_titles[id_[1]] = target_book.get_category()
    return _make_response(json.dumps({
                'titles': book_titles
            }))

@app.route('/searchword/', methods=['GET'])
def search_keyword():
    book_titles = {}
    book_ids = books.book().search_ids(request.args.get('keyword'))
    for id_ in book_ids:
        target_book = books.book(id_=id_)
        book_titles[target_book.get_title(True)] = target_book.get_categories()
    return _make_response(json.dumps({
                'titles': book_titles
            }))

@app.route('/getlist/', methods=['GET'])
def get_all():
    book_titles = []
    cate = []
    uploaddates = []
    ids_category = books.book().get_categories()
    book_ids = books.book().get_all_ids()
    for count, id_ in enumerate(book_ids):
        book_titles.append(id_[1])
        uploaddates.append(id_[2].split('T')[0])
        if int(id_[0]) not in ids_category:
            cate.append([])
            continue
        cate.append(ids_category[int(id_[0])])
    return _make_response(json.dumps({
                'titles': book_titles,
                'category': cate,
                'uploaddate': list(sorted(list(set(uploaddates))))
            }))

@app.route('/getlist_cate/', methods=['GET'])
def get_allcategory():
    return _make_response(json.dumps({
                'categories': categories.category().get_all_name()
            }))

@app.route('/autodeploy/', methods=['POST'])
def autodeploy():
    import subprocess
    if "master" in request.json['ref']:
        subprocess.call(['git', 'fetch', 'origin'])
        subprocess.call(['git', 'merge', 'origin/master'])
        cmd = "ps aux | grep server.py"
        pid = subprocess.check_output(cmd , shell=True)
        for line in str(pid).split('\\n')[:-1]:
            if ('grep' not in line) and ('0:01' not in line):
                subprocess.call('kill', '-9', str(line.split('    ')[1].split('  ')[0]))
                subprocess.call(['nohup', 'python', 'server.py', '&'])
    return _make_response()

@app.route('/download/', methods=['GET'])
def file_download():
    import platform
    import subprocess
    from smb.SMBConnection import SMBConnection
    user = 't-hayashi'
    password = 'tomonori'
    conn = SMBConnection(
        user,
        password,
        platform.uname().node,
        'yellow',
        domain='wsl',
        use_ntlm_v2=True
    )
    conn.connect('192.168.60.10', 139)
    items = conn.listPath('PUBLIC', 'scansnap')
    yellow_num = list(filter(lambda x: '.pdf' in x, [item.filename for item in items]))
    db_num = []
    with open('yellow_filenames.csv') as f:
        for name in f:
            db_num.append(name[:-1])
    with open('./yellow_filenames.csv', 'w') as f:
        for name in yellow_num:
            f.write(name + '\n')
    if len(yellow_num) > len(db_num):
        mes = 'http://http://192.168.60.62:10080/ \n以下のPDFが追加されました。\n'
        dif_names = list(set(yellow_num).difference(set(db_num)))
        for name in dif_names:
            mes += name[:-4] + '\n'
            with open('./test_dlPDF/' + name, 'wb') as file:
                conn.retrieveFile('PUBLIC', 'scansnap/' + name, file)
            subprocess.call(["zip", '--junk-paths', 'file', './test_dlPDF/' + name, name, './test_dlPDF/' + name])
            subprocess.call(["mv", 'file.zip', './test_dlPDF/' + name + '.zip'])
            books.book(title=name[:-4]).add_title()

        requests.post('https://hooks.slack.com/services/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', data = json.dumps({
            'text': mes, # 投稿するテキスト
            'username': 'WSL Degital Library' # 投稿のユーザー名
        }))
        return _make_response(json.dumps({
                    'message': mes + 'のアップロードが完了しました'
                }))
    return  _make_response(json.dumps({
                'message': ''
            }))

def _make_response(json_data=None):
    response = make_response(json_data)
    response.headers["Content-Type"] = "application/json"
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    app.run(host=ENV[0][1], port=int(ENV[1][1]), processes=6)
