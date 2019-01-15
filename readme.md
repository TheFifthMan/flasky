# 初始化 flask 环境
```
pip install pipenv 
mkdir flasky
pipenv shell
pipenv install flask
# 安装插件
pipenv install flask-sqlalchemy flask-migrate flask-wtf flask-mail pymysql
mkdir app
```
创建 .env 文件，在使用pipenv的时候会载入.env 文件
```
# .env
FLASK_APP=run.py
FLASK_DEBUG = 1
```
# app初始化
新建初始化文件,使用工厂函数来创建 app 以便后续写unittest的时候，能够动态的传入不同的配置，从而生成 app 实例。
```py
# app/__init__.py
from flask import Flask 
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_mail  import Mail

# 数据库连接
db = SQLAlchemy()
# 发送邮件
mail = Mail()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # 初始化各种插件
    config[config_name].init_app(app)
    db.init_app(app)
    mail.init_app(app)

    return app
```
# 配置文件初始化
新建config.py
```py

# config.py
# coding: utf-8
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
        
class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_SQLALCHEMY_DATABASE_URI") or "mysql+pymysql://root:qwe123@127.0.0.1/flasky"

class TestingConfig(Config):
    Testing = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_SQLALCHEMY_DATABASE_URI") or "mysql+pymysql://root:qwe123@127.0.0.1/flasky"

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI") or "mysql+pymysql://root:qwe123@127.0.0.1/flasky"


config = {
    "dev":DevConfig,
    "test":TestingConfig,
    "prod":ProdConfig,
    "default":DevConfig
}
```
添加内容到 .env 文件
```
# .env
...
SECRET_KEY = 81785a8c-1f9a-4cfb-bc9d-90a8374bbc15 
MAIL_SERVER = xxx
MAIL_PORT = xxx
MAIL_USE_TLS = xx
MAIL_USERNAME = tester
MAIL_PASSWD = qwe123
DEV_SQLALCHEMY_DATABASE_URI= xxx
TEST_SQLALCHEMY_DATABASE_URI=xxx
SQLALCHEMY_DATABASE_URI = xxx
```
# 初始化log
当应用运行起来的时候，最佳的做法不应该将错误信息直接输出到页面上让用户看到，这样做既不专业，也不安全。最佳的做法是当应用发生错误的时候，应该直接将用户导向 500 页面，然后将发生的错误使用log记录下来供开发进行调查。

```py
# app/__init__.py
from logging.handlers import SMTPHandler,RotatingFileHandler

def create_app(config_name):
    ...
    if not app.debug:
        
        # 记录到文件
        if not os.path.exists('logs'):
                    os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/flasky.log',maxBytes=10240,backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('app start.')

        # 发送邮件，可不设置
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWD']:
            auth = (app.config['MAIL_USERNAME'],app.config['MAIL_PASSWD'])
        secure = None
        if app.config['MAIL_USE_SSL']:
            secure = ()
        
        mail_handler = SMTPHandler(
                mailhost=app.config['MAIL_SERVER'],
                fromaddr=app.config['MAIL_USERNAME'],
                toaddrs=app.config['ADMINS'],
                subject="flasky Error",
                credentials=auth,secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
```

# 蓝图 / 即插视图
使用功能模块来分割蓝图，使用即插视图来分离路由和逻辑处理。方便代码管理。
新建 index 文件夹，并添加 __init__.py 文件

```py
# index/__init__.py
from flask import Blueprint
index_bp = Blueprint("index",__name__)
from . import views,routes

# index/views.py
from flask.views import MethodView 
from flask import render_template
class Index(MethodView):
    def get(self):
        return render_template("index.html")

# index/routes.py
from index import index_bp
from index.views import Index

index_bp.add_url_rule('/',view_func=Index.as_view('index'))

# 当需要url_for 的时候，可以使用 index 这个名字 index.index
# url_for('index.index') index 可以类比为就是这个函数的名字
```
以上完成了一个蓝图的基本设置。接下来添加蓝图到app实例

```py
# app/__init__.py
def create_app(config_name):
    ...
    from app.index import index_bp 
    app.register_blueprint(index_bp)
    ...
    return app
```
# 测试
测试初始化功能是否正常
```
pipenv shell
flask run 
```
打开 http://localhost:5000 查看是否存在错误



代码地址：https://github.com/TheFifthMan/flasky
# 参考
推荐阅读： 《OReilly.Flask.Web.Development.2nd.Edition》