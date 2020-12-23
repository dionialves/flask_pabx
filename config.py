import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    DEBUG = True
    SECRET_KEY = 'ndnekfmermfgwnrfnenwgjvrews'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'storage.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASK_ENV = 'development'
