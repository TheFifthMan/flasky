from .config impirt Config
class DevConfig(Config):
    DEBUG = True
    ADMIN = os.getenv("DEV_ADMIN")
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_SQLALCHEMY_DATABASE_URI") or "mysql+pymysql://root:qwe123@127.0.0.1/flasky"
