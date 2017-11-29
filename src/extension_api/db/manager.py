from .schema import books, pages, vectors, Session
session = Session()
# DBと接続を行う系のものはこっちで
import json


class DBManager(object):
    """docstring for DBManager"""

    def __init__(self):
        super(DBManager, self).__init__()

    @staticmethod
    def post_book(name, raw_pages_texts, parsed_pages_texts,
                  parsed_pages_vecs, **keywords):
        """
        Function: post_book
        Summary: 本をDBに保存
        Attributes:
          @param (name):本の名前
          @param (raw_pages_texts):ページ毎のテキストリスト["page1_text", "page2_text",...]
          @param (parsed_pages_texts):ページ毎の整形済みテキストリスト
        """
        vec_type_name = keywords.get("vec_type_name", "lda")

        _book = books(name=name)
        _pages = [pages(number=i, raw_text=raw_text,
                        parsed_text=parsed_text,
                        vector=[vectors(
                            vec_type=vec_type_name,
                            vector=json.dumps(_vec.tolist())
                        )])
                  for i, (raw_text, parsed_text, _vec)
                  in enumerate(zip(raw_pages_texts,
                                   parsed_pages_texts,
                                   parsed_pages_vecs))]
        _book.pages = _pages
        session.add(_book)
        session.commit()

    @staticmethod
    def load_page_text(book_name, page_id):
        pass

    @staticmethod
    def load_vec_list(book_id=None, page_id=None, limit=None, offset=None):
        query = session.query(vectors)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        return query

    @staticmethod
    def load_page_by_vec_list(vec_list):
        _page_ids = [v.page_id for v in vec_list]
        _pages = session.query(pages).filter(pages.id in _page_ids).all()
        return _pages
