import os 

class Config(object):
    SECRET_KEY = os.getenv('SECRET')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWD = os.getenv("MAIL_PASSWD")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def init_app(self):
        pass