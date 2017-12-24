from sqlalchemy import Column, Integer, String, Text, Float, DATETIME, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.schema import UniqueConstraint
from datetime import datetime
from config import config
import json
import numpy as np
from logger import get_module_logger
logger = get_module_logger(__name__)
Base = declarative_base()


class books(Base):
    """本テーブル"""
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    pages = relationship('pages')
    vectors = relationship('vectors')
    categories = relationship('books_categories')
    created = Column('created', DATETIME, default=datetime.now, nullable=False)
    modified = Column('modified', DATETIME,
                      default=datetime.now,
                      onupdate=datetime.now,
                      nullable=False)

    def __repr__(self):
        return '<books(%d)>' % (self.name)


class pages(Base):
    """ページテーブル"""
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey(
        "books.id", onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    number = Column(Integer)
    raw_text = Column(Text)
    parsed_text = Column(Text)
    vector = relationship('vectors')
    created = Column('created', DATETIME, default=datetime.now, nullable=False)
    modified = Column('modified', DATETIME,
                      default=datetime.now,
                      onupdate=datetime.now,
                      nullable=False)

    def __repr__(self):
        return '<pages(book:%d, number:%d, text:(%s))>' % \
            (self.book_id, self.number, self.text[:10])


class vectors(Base):
    """ベクトルテーブル"""
    __tablename__ = 'vectors'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id", onupdate='CASCADE',
                                         ondelete='CASCADE'), nullable=True)
    page_id = Column(Integer, ForeignKey("pages.id", onupdate='CASCADE',
                                         ondelete='CASCADE'), nullable=True)
    vec_type = Column(String(30))
    vector = Column(Text)
    created = Column('created', DATETIME, default=datetime.now, nullable=False)
    modified = Column('modified', DATETIME,
                      default=datetime.now,
                      onupdate=datetime.now,
                      nullable=False)

    def get_np_vector(self):
        _vec = json.loads(self.vector)
        return np.array(_vec)

    def cos_sim(self, with_vec):
        v1 = self.get_np_vector()
        if isinstance(with_vec, vectors):
            v2 = with_vec.get_np_vector()
        else:
            v2 = with_vec

        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    def __repr__(self):
        return '<vectors(book:{}, page:{}, type:{})>'.format(
            self.book_id, self.page_id, self.vec_type
        )


class categories(Base):
    """カテゴリテーブル"""
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    books = relationship('books_categories')
    # book_id = Column(Integer, ForeignKey(
    #     "books.id", onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    created = Column('created', DATETIME, default=datetime.now, nullable=False)
    modified = Column('modified', DATETIME,
                      default=datetime.now,
                      onupdate=datetime.now,
                      nullable=False)

    def __repr__(self):
        return '<categories(name:%s, book:%d)>' % \
            (self.name, self.book_id)


class books_categories(Base):
    """本とカテゴリの紐付けテーブル"""
    __tablename__ = 'books_categories'
    book_id = Column(Integer, ForeignKey(
        "books.id", onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True)
    category_id = Column(Integer, ForeignKey(
        "categories.id", onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True)
    # book = relationship(books, backref='book_junctions')
    # category = relationship(categories, backref='category_junctions')

# SQLに接続。
_pass = config['db']['PASS']
if _pass != "":
    _pass = ":" + _pass
url = '{}://{}{}@{}/{}?charset=utf8'.format(config['db']['DBMS'],
                                            config['db']['USER'],
                                            _pass,
                                            config['db']['HOST'],
                                            config['db']['DB'])
logger.debug(url)
engine = create_engine(url, echo=True, pool_recycle=1000)

if config['db']['INIT_DB'] == 'True':
    engine.execute('SET FOREIGN_KEY_CHECKS=0;')
    engine.execute('DROP TABLE IF EXISTS {}'.format("books"))
    engine.execute('DROP TABLE IF EXISTS {}'.format("pages"))
    engine.execute('DROP TABLE IF EXISTS {}'.format("vectors"))
    engine.execute('DROP TABLE IF EXISTS {}'.format("categories"))
    engine.execute('DROP TABLE IF EXISTS {}'.format("books_categories"))
    engine.execute('SET FOREIGN_KEY_CHECKS=1;')


# テーブル作成
Base.metadata.create_all(engine)
# セッションの作成
Session = sessionmaker(bind=engine)
# session = Session()
