#!flask/bin/python
# -*- coding: utf-8 -*-

from app import app
from app.database import init_db, db_session
from app.models import Book, Author

init_db()

q_author = Author(name=u'Фрэнк Херберт')
q_author.books.append(Book(name=u'Дюна'))
db_session.add(q_author)

q_author = Author(name=u'Толкин')
q_author.books.append(Book(name=u'Властелин колец'))
db_session.add(q_author)

q_author = Author(name=u'Макс Фрай')
q_author.books.append(Book(name=u'Лабиринты Эхо'))
db_session.add(q_author)

q_author = Author(name=u'Ник Перумов')
q_author.books.append(Book(name=u'Алмазный меч, деревянный меч'))
db_session.add(q_author)

q_author = Author(name=u'Фридрих Ницше')
q_author.books.append(Book(name=u'Так говорил Заратустра.'))
db_session.add(q_author)

db_session.commit()


exit()