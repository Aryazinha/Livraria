import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '93674838d1b41e668ccb0ca548dc220e924450bac6596aef7bdab8d17c6d5d91'
    # Aponta diretamente para dentro da pasta instance
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'bookstorage.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False