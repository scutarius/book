# -*- coding: utf-8 -*-

from flask import Flask

from .database import init_db

from flask.ext.login import LoginManager



app = Flask(__name__)
app.config.from_object('config')


init_db()

lm = LoginManager(app)

from app import views, models
