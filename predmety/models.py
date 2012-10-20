
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

def repr(self):
    return "%s(%s)" % (
        self.__class__.__name__,
        ', '.join(["%s=%r" % (key, getattr(self, key))
                   for key in sorted(self.__dict__.keys())
                   if not key.startswith('_')]))
Base.__repr__ = repr


class Link(Base):
    __tablename__ = 'link'
    code = Column(String(255), nullable=False, primary_key=True)
    redirect = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())


class Suggestion(Base):
    __tablename__ = 'suggestion'
    id = Column(Integer, nullable=False, primary_key=True)
    code = Column(String(255), nullable=False)
    redirect = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())


class Moderator(Base):
    __tablename__ = 'moderator'
    user = Column(String(255), primary_key=True)


def create_tables(engine):
    Base.metadata.create_all(engine)
