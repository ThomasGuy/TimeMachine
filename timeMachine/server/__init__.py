import logging

# third party imports
from flask import Flask
from flask_sqlalchemy_session import flask_scoped_session
from flask_login import LoginManager

# package imports
from timeMachine.config import Config

log = logging.getLogger(__name__)


login = LoginManager()
login.login_view = 'auth.login'


from timeMachine.database.base import session_factory


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    flask_scoped_session(session_factory, app)

    login.init_app(app)

    from timeMachine.server.errors import bp as error_bp
    app.register_blueprint(error_bp)

    from timeMachine.server.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from timeMachine.server.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app


from timeMachine.database import models
