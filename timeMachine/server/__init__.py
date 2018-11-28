import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

# third party imports
from flask import Flask
from flask_sqlalchemy_session import flask_scoped_session
from flask_login import LoginManager
from flask_mail import Mail

# package imports
from timeMachine.config import Config

log = logging.getLogger(__name__)


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
# mail = Mail()


def create_app(config_class=Config):
    app = Flask('timeMachine.server')
    app.config.from_object(Config)

    from timeMachine.database.base import session_factory, BaseModel
    Session = flask_scoped_session(session_factory, app)
    BaseModel.set_session(Session)

    login_manager.init_app(app)
    # mail.init_mail(app)

    from timeMachine.server.errors import bp as error_bp
    from timeMachine.server.auth import bp as auth_bp
    from timeMachine.server.main import bp as main_bp
    app.register_blueprint(error_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    from TickTocTest.ticktoctest.models import User
    from flask_sqlalchemy_session import current_session as cs

    @login_manager.user_loader
    def load_user(id):
        return cs.query(User).get(int(id))

    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.DEBUG)
            # app.logger.addHandler(mail_handler)
            log.addHandler(mail_handler)

    return app, Session


from timeMachine.database import models
