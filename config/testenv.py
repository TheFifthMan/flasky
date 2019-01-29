import os 
from .config impirt Config

class TestingConfig(Config):
    Testing = True
    ADMIN = os.getenv("TEST_ADMIN")
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_SQLALCHEMY_DATABASE_URI") or "mysql+pymysql://root:qwe123@127.0.0.1/flasky"
