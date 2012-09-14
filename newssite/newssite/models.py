import re
import unicodedata

from sqlalchemy import (
    Column,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    DateTime,
    Boolean,
    )

from zope.sqlalchemy import ZopeTransactionExtension
from pyramid.traversal import resource_path

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

def _slugify(value):
    value = value.replace('ł', 'l')
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = value.decode('ascii')
    return re.sub('\W+', '-', value.lower())

class TraversalStep:
    def __init__(self, request, name='', parent=None):
        self.request = request
        self.__name__ = name
        self.__parent__ = parent

    def __getitem__(self, key):
        try:
            result = DBSession.query(self.model).filter(
                getattr(self.model, self.lookup_key)==key
            ).one()
            result.__parent__ = self
            return result
        except NoResultFound:
            raise KeyError

class Root(TraversalStep):

    def __getitem__(self, key):
        if key == 'news':
            return NewsCollection(self.request, 'news', self)
        elif key == 'users':
            return UsersCollection(self.request, 'users', self)
        raise KeyError()


class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    title = Column(String(64), unique=True)
    slug = Column(String(64), unique=True)
    content = Column(Text)
    published = Column(DateTime)
    accepted = Column(Boolean)
    

    def __init__(self, title, content, published):
        self.title = title
        self.slug = _slugify(title)
        self.content = content
        self.published = published
        self.accepted = False

    def get_link(self):
        return resource_path(self)

    @property
    def __name__(self):
        return self.slug


class NewsCollection(TraversalStep):
    model = News
    lookup_key = 'slug'

    def get_index(self):
        news = DBSession.query(News).order_by(News.published).all()
        for news_item in news:
            news_item.__parent__ = self
        return news
