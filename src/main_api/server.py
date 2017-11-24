from flask import Flask, request, jsonify, make_response
from models import books, categories
import codecs
import json
import configparser
import dataset

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
    ids_category = books.book().get_categories()
    book_ids = books.book().get_all_ids()
    for count, id_ in enumerate(book_ids):
        book_titles.append(id_[1])
        if int(id_[0]) not in ids_category:
            cate.append([])
            continue
        cate.append(ids_category[int(id_[0])])
    return _make_response(json.dumps({
                'titles': book_titles,
                'category': cate
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
                cmd1 = 'nohup python server.py &'
                subprocess.call(cmd1, shell=True)
    return _make_response()


@app.route('/upload/', methods=['POST'])
def file_upload():
  import subprocess
  new = []
  if request.files.getlist('upload_files')[0].filename:
      upload_files = request.files.getlist('upload_files')
      for upload_file in upload_files:
          new.append(upload_file.filename)
          upload_file.save("./dlPDF/" + upload_file.filename)
          subprocess.call(["zip", '--junk-paths', 'file', './dlPDF/' + upload_file.filename, upload_file.filename, './dlPDF/' + upload_file.filename])
          subprocess.call(["mv", 'file.zip', './dlPDF/' + upload_file.filename + '.zip'])
  asd = []
  asdd = []
  with open('./PDF_list_column.txt') as g:
      for lines in g:
          asd.append(lines[:-1])
  asd += new
  with open('./PDF_list_column.txt', 'w') as g:
      for name in asd:
          g.write(name + '\n')

  with open('./PDF_list.txt') as g:
      for lines in g:
          asdd.append(lines[:-1])
  asdd += new
  with open('./PDF_list.txt', 'w') as g:
      for name in asdd:
          g.write(name + '\n')
  return _make_response()

def _make_response(json_data=None):
    response = make_response(json_data)
    response.headers["Content-Type"] = "application/json"
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    app.run(host=ENV[0][1], port=int(ENV[1][1]))
