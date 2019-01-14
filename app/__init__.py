from flask import Flask 
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_mail  import Mail

db = SQLAlchemy()
mail = Mail()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # 初始化各种插件
    config[config_name].init_app(app)
    db.init_app(app)
    mail.init_app(app)
    from app.index import index_bp 
    app.register_blueprint(index_bp)
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

        # 发送邮件
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWD']:
            auth = (app.config['MAIL_USERNAME'],app.config['MAIL_PASSWD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        
        mail_handler = SMTPHandler(
                mailhost=app.config['MAIL_SERVER'],
                fromaddr=app.config['MAIL_USERNAME'],
                toaddrs=app.config['ADMINS'],
                subject="Error log",
                credentials=auth,secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


    return app
