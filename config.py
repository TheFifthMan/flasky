# coding: utf-8
import os 

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWD = os.getenv("MAIL_PASSWD")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def init_app(self):
        pass
        
class DevConfig(Config):
    DEBUG = True
    ADMIN = os.getenv("DEV_ADMIN")
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_SQLALCHEMY_DATABASE_URI") or "mysql+pymysql://root:qwe123@127.0.0.1/flasky"

class TestingConfig(Config):
    Testing = True
    ADMIN = os.getenv("TEST_ADMIN")
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_SQLALCHEMY_DATABASE_URI") or "mysql+pymysql://root:qwe123@127.0.0.1/flasky"

class ProdConfig(Config):
    ADMIN = os.getenv("ADMIN")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI") or "mysql+pymysql://root:qwe123@127.0.0.1/flasky"


config = {
    "dev":DevConfig,
    "test":TestingConfig,
    "prod":ProdConfig,
    "default":DevConfig
}