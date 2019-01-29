import os 
from .config impirt Config

class ProdConfig(Config):
    ADMIN = os.getenv("ADMIN")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI") or "mysql+pymysql://root:qwe123@127.0.0.1/flasky"
