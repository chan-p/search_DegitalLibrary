# -*- coding: utf-8 -*-
from flask import Flask, jsonify, abort, make_response, request, redirect, url_for
from config import config
from logger import get_module_logger
from pdf_converter import PDFConverter
from db.manager import DBManager
from text_parser import TextParser
import traceback
from vectorizer import LDAVectorizer as Vectorizer

pdf_converter = PDFConverter()
text_parser = TextParser()
logger = get_module_logger(__name__)
api = Flask(__name__)


@api.route('/')
def index():
    return redirect(url_for('recommend'))


@api.route('/search/<doc>/<key>', methods=['GET'])
def search(doc, key):
    if key == "url":
        # TODO: URLで検索する時。URL先をスクレイピング、ベクトル化、類似度計算を行う。
        return _tbd_response("スクレイピングによる検索")
    elif key == "keyword":
        # キーワード検索
        if doc == "page":
            # ページの検索
            _keyword = request.args.get('q')
            _limit, _offset = args_get_op_param()
            # キーワードをベクトル化
            _vectorizer = Vectorizer.load(config['api']['MODEL_PATH'])
            _t_vec = _vectorizer.vectorize(_keyword)
            # DBからベクトルリストを持ってくる
            _vec_list = DBManager.load_vec_list(limit=_limit, offset=_offset)
            _similar_vec_list = Vectorizer.sort_by_similar(_t_vec, _vec_list)
            _page_ids = [v.page_id for v in _similar_vec_list]
            # _similar_page_list = load_page_by_vec_list(_similar_vec_list)
            return _success_response({"page_ids": _page_ids})
        elif doc == "book":
            # 本の検索
            return _tbd_response("本の類似度検索")
    return _error_response()


def args_get_op_param():
    limit = request.args.get('limit', None, type=int)  # 数
    offset = request.args.get('offset', None, type=int)  # 始点
    return limit, offset


@api.route('/notify_upload', methods=['GET'])
def notify_upload():
    # アップロードが検知されたら呼び出される。
    # ここで、対象の本を受け取り、ベクトル化、DBへ格納する。
    target_books = request.args.getlist('upload_files[]', type=str)
    logger.debug(target_books)
    for target_book in target_books:
        _after_upload_book(target_book)
    return _success_response({"res": "OK"})


def _after_upload_book(name):
    # 本のアップロード後に呼び出される。
    # 1.まず、対象の本のPDFを読み込み、素のテキストをDBに格納。
    _path = config['pdf']['DIR'] + name
    _name = name.replace(".pdf", "")
    _raw_pages_texts = pdf_converter.read_by_page(_path)
    _parsed_pages_texts = text_parser.parse(_raw_pages_texts)

    # 2.読み取ったテキストをコーパスに追加し、モデルを更新
    _save_name = config['api']['TEXTS_PATH_NAME']
    _vectorizer = Vectorizer(_parsed_pages_texts,
                             topic_N=20,
                             no_below=3,
                             no_above=0.6,
                             load_name=_save_name,
                             save_name=_save_name)
    _vectorizer.save(config['api']['DATA_DIR'])

    # 3.ベクトル化を行い、DBへ
    _vec_list = [_vectorizer.vectorize(text) for text in _parsed_pages_texts]
    DBManager.post_book(_name, _raw_pages_texts,
                        _parsed_pages_texts, _vec_list,
                        vec_type_name=_vectorizer.get_vec_type_name())

# ---------------レスポンス系--------------------


def _tbd_response(name=None):
    # To Be Developed(要実装)
    if name is not None:
        name += "は"
    else:
        name = ""
    return _success_response({"無理です": "{}は実装中です。ごめんね！".format(name)})


def _error_response(e, _dict=None):
    _error_message = traceback.format_exc()
    logger.error(_error_message)
    abort(400)


def _success_response(_dict=None):
    result = _make_message("OK", "None", _dict)
    return _make_json_response(result)


def _make_json_response(result):
    response = make_response(jsonify(result))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


def _make_message(state, _state_msg, _dict):
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
    print("api starting...(host:{host},port:{port}"
          .format(host=host, port=port))
    api.run(host=host, port=port)
