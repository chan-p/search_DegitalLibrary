# -*- coding: utf-8 -*-
from flask import Flask, jsonify, abort, make_response, request, redirect, url_for
from config import config
from logger import get_module_logger
from pdf_converter import PDFConverter
from db.manager import DBManager

db = DBManager()
converter = PDFConverter()
logger = get_module_logger(__name__)
api = Flask(__name__)

@api.route('/')
def index():
  return redirect(url_for('recommend'))

@api.route('/search/<command>', methods=['GET'])
def search():
  if command == "url":
    # TODO: URLで検索する時。URL先をスクレイピング、ベクトル化、類似度計算を行う。
    pass
  elif command == "keyword":
    # TODO: キーワードで検索する時。
    pass
  return _success_response({"res":"OK"})

@api.route('/notify_upload', methods=['GET'])
def notify_upload():
  # アップロードが検知されたら呼び出される。
  # ここで、対象の本を受け取り、ベクトル化、DBへ格納する。
  target_books = request.args.getlist('upload_files[]',type=str)
  logger.debug(target_books)
  for target_book in target_books:
    after_upload_book(target_book)
  return _success_response({"res":"OK"})

def after_upload_book(name):
  # 本のアップロード後に呼び出される。
  # まず、対象の本のPDFを読み込み、素のテキストをDBに格納。
  _path = config['pdf']['DIR']+name
  _name = name.replace(".pdf","")
  _pages_texts = converter.read_by_page(_path)
  db.post_book(_name, _pages_texts)

# ---------------レスポンス系--------------------
def _error_response(e,_dict=None):
  _error_message = traceback.format_exc()
  logger.error(_error_message)
  abort(400)

def _success_response(_dict=None):
  result = _make_message("OK","None",_dict)
  return _make_json_response(result)

def _make_json_response(result):
  response = make_response(jsonify(result))
  response.headers['Access-Control-Allow-Origin'] = '*'
  return response

def _make_message(state,_state_msg,_dict):
  result = {
  "ret":            state,
  "error_message":  _state_msg
  }
  if _dict is not None:
    result.update(_dict)
  return result


if __name__ == '__main__':
  host = config['api']['HOST']
  port = config['api']['PORT']
  print("api starting...(host:{host},port:{port}"\
    .format(host=host, port=port))
  api.run(host=host, port=port)