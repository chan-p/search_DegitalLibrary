from .schema import books, pages, vectors, Session
session = Session()
# DBと接続を行う系のものはこっちで

class DBManager(object):
  """docstring for DBManager"""
  def __init__(self):
    super(DBManager, self).__init__()

  def post_book(self, name, pages_texts):
    """
    Function: post_book
    Summary: 本をDBに保存
    Attributes: 
      @param (name):本の名前
      @param (pages_texts):ページ毎のテキストリスト
    """
    _book = books(name=name)
    _pages = [pages(number=i, text=_text) for i, _text in enumerate(pages_texts)]
    _book.pages = _pages
    session.add(_book)
    session.commit()