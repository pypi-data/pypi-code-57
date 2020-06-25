from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)
    timestamp = Column(DateTime)
    addresses = relationship("Adress")


class Adress(Base):
    __tablename__ = "adress"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    foos = relationship("Foo")


class Foo(Base):
    __tablename__ = "foo"
    id = Column(Integer, primary_key=True)
    foo = Column(String)
    adress_id = Column(Integer, ForeignKey("adress.id"))
    bars = relationship("Bar")


class Bar(Base):
    __tablename__ = "bar"
    id = Column(Integer, primary_key=True)
    bar = Column(String)
    foo_id = Column(Integer, ForeignKey("foo.id"))
