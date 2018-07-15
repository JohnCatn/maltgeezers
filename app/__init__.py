import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_user import UserManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_scss import Scss
from config import Config


db = SQLAlchemy()
migrate = Migrate()

mail = Mail()
bootstrap = Bootstrap()
moment = Moment()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.json_encoder = MaltgeezersJSONEncoder
    app.config.from_object(config_class)
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    if not os.path.exists('logs'):
        os.mkdir('logs')
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.mkdir(app.config['UPLOAD_FOLDER'])
    file_handler = RotatingFileHandler('logs/maltgeezers.log',
                                       maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('beginning startup')

    Scss(app)
    db.init_app(app)
    migrate.init_app(app, db)
    # Setup Flask-User and specify the User data-model
    user_manager = MaltgeezersUserManager(app, db, User)
    #user_manager = UserManager(app, db, User)
#    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Maltgeezers Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        app.logger.info('Maltgeezers startup')

    return app

from app.models import User
from app.main.forms import MaltgeezersUserManager
from app.main.routes import MaltgeezersJSONEncoder
