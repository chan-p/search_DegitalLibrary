from flask import Flask, request, jsonify, make_response
from models import books
import codecs
import json
import configparser

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('./setting.ini')
ENV = config.items('LOCALTEST')

@app.route('/', methods=['GET'])
def update_PDFlist():
    title = request.args.get('title').encode('utf-8').decode('utf-8')
    column = request.args.get('column')
    line = []
    flg = 0
    with codecs.open('./PDF_list_column.txt', 'r', 'utf-8') as f:
        for li in f:
            lis = li[:-1].split(',')
            rr = li[:-1]
            if title == lis[0]:
                rr += ',' + column
            line.append(rr + '\n')
    with codecs.open('./PDF_list_column.txt', 'w', 'utf-8') as g:
        for jj in line:
            g.write(jj)
    return _make_response()

@app.route('/delete/', methods=['GET'])
def delete_cate():
    title = request.args.get('title').encode('utf-8').decode('utf-8')
    column = request.args.get('column')
    line = []
    flg = 0
    with codecs.open('./PDF_list_column.txt', 'r', 'utf-8') as f:
        for li in f:
            lis = li[:-1].split(',')
            rr = li[:-1]
            if title == lis[0]:
                lis.remove(column)
                print(lis)
            line.append(",".join(lis) + '\n')
    with codecs.open('./PDF_list_column.txt', 'w', 'utf-8') as g:
        for jj in line:
            g.write(jj)
    return _make_response()

@app.route('/update/', methods=['GET'])
def update_cate():
  dic = {}
  with open('./PDF_list_column.txt') as g:
    for lines in g:
      line = lines[:-1].split(',')
      for cate in line[1:]:
        if cate not in dic:
          dic[cate] = []
        dic[cate].append(line[0])

  with open('./cate_search.txt', 'w') as g:
    for i, v in dic.items():
      g.write(i)
      for ca in v:
        g.write(',' + ca)
      g.write('\n')

  g = open('./column_list.txt', 'w')
  column_list = []
  with open('./PDF_list_column.txt') as f:
    for lines in f:
      line = lines[:-1].split(',')
      for co in line[1:]:
        if co not in column_list:
          column_list.append(co)

  for ii in column_list:
    g.write(ii + '\n')
  g.close()
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

@app.route('/getlist/', methods=['GET'])
def get_allPDF():
    bks = books.books()
    return _make_response(json.dumps({
                'pdfs': bks.get_all_title()
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

def _make_response(json_data=None):
    response = make_response(json_data)
    response.headers["Content-Type"] = "application/json"
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    app.run(host=ENV[0][1], port=int(ENV[1][1]))
