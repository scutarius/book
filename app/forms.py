# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import validators
from wtforms.fields import TextField, BooleanField, PasswordField

from models import User

class LoginForm(Form):
    login = TextField(u'login', [validators.Length(min=4, max=25)])
    password=PasswordField(u'password')
    remember_me = BooleanField('remember_me', default = False)

    def validate(self):
        login = Form.validate(self)
        if not login:
            return False

        user = User.query.filter_by(login=self.login.data).first()
        if user is None:
            self.login.errors.append(u'Неверный логин')
            return False
        else:
            self.password.errors.append(u'Неверный пароль')

        self.user = user
        return True

class RegForm(Form):
    login     = TextField(u'Логин', [validators.Length(min=4, max=25)])
    password1 = PasswordField(u'Новый пароль', [
        validators.Required(message=u'Пустое поле'),
        validators.EqualTo('password2', message=u'Пароли должны совпадать'),
        validators.Length(min=6, max=30, message=u'Пароль должен быть в пределах 6<pass<30')
        ])
    password2 = PasswordField(u'Повторить пароль', [validators.Required(message=u'Пустое поле')])
    email = TextField(u'Email адресс', [
        validators.Email(message=u'Неверное имя почты'),
        ])

class BookUpload(Form):
    title = TextField(u'title')
    author = TextField(u'author')

class SearchForm(Form):
    search = TextField(u'search')

class EditAutor(Form):
    author = TextField(u'author')

class EditBook(Form):
    book = TextField(u'book')