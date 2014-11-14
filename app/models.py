# -*- coding: utf-8 -*-

from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(50), unique=True)
    password = Column(String(64))
    email = Column(String(120), unique=True)

    def __init__(self, login=None, password=None, email=None):
        self.login = login
        self.password = password
        self.email = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.login)


association_table = Table('association', Base.metadata,
    Column('authors_id', Integer, ForeignKey('authors.id')),
    Column('books_id', Integer, ForeignKey('books.id'))
)


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))

    books = relationship("Book", secondary = "association", backref="authors")

    def __repr__(self):
        return u'<Author %r>' % (self.name)


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))

    def __repr__(self):
        return u'<Book %r>' % (self.name)

