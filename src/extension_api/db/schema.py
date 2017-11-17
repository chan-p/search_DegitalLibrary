from sqlalchemy import Column, Integer, String, Text, Float, DATETIME, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.schema import UniqueConstraint
from datetime import datetime
from config import config
from logging import getLogger
logger = getLogger(__name__)
Base = declarative_base()

class books(Base):
  """ユーザ情報テーブル定義"""
  __tablename__ = 'books'
  id = Column(Integer, primary_key=True)
  name = Column(String(100),unique=True)
  pages = relationship('pages')
  vectors = relationship('vectors')
  created = Column('created', DATETIME, default=datetime.now, nullable=False)
  modified = Column('modified', DATETIME, default=datetime.now, nullable=False)

  def __repr__(self):
    return '<books(%d)>' % (self.name)

class pages(Base):
  """DBテーブル定義"""
  __tablename__ = 'pages'
  id = Column(Integer, primary_key=True)
  book_id = Column(Integer, ForeignKey("books.id", onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
  number = Column(Integer)
  text = Column(Text)
  created       = Column('created', DATETIME, default=datetime.now, nullable=False)
  modified      = Column('modified', DATETIME, default=datetime.now, nullable=False)

  def __repr__(self):
    return '<pages(book:%d, number:%d, text:(%s))>' % \
    (self.book_id, self.number, self.text[:10])

class vectors(Base):
  """DBテーブル定義"""
  __tablename__ = 'vectors'
  id = Column(Integer, primary_key=True)
  book_id = Column(Integer, ForeignKey("books.id", onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
  page_id = Column(Integer, ForeignKey("pages.id", onupdate='CASCADE', ondelete='CASCADE'), nullable=True)
  vec_type = Column(String(30))
  vec_target = Column(String(30))
  vector = Column(Text)
  created       = Column('created', DATETIME, default=datetime.now, nullable=False)
  modified      = Column('modified', DATETIME, default=datetime.now, nullable=False)

  def __repr__(self):
    return '<vectors(book:%d, page:%d, type:%s, target:%s)>' % \
    (self.book_id, self.page_id, self.vec_type, self.vec_target)

# SQLに接続。
url = '{}://{}:{}@{}/{}?charset=utf8'.format(config['db']['DBMS'],config['db']['USER'],config['db']['PASS'],config['db']['HOST'],config['db']['DB'])
logger.debug(url)
engine = create_engine(url, echo=True)

if config['db']['INIT_DB']=='True':
  engine.execute('DROP TABLE IF EXISTS {}'.format("books"))
  engine.execute('DROP TABLE IF EXISTS {}'.format("pages"))
  engine.execute('DROP TABLE IF EXISTS {}'.format("vectors"))

# テーブル作成
Base.metadata.create_all(engine)
# セッションの作成
Session = sessionmaker(bind=engine)
# session = Session()