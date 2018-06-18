# Third party imports
from flask import render_template
from flask_sqlalchemy_session import current_session

# package imports
from timeMachine.server.errors import bp
# from timeMachine import session as db


@bp.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@bp.errorhandler(500)
def internal_error(error):
    current_session.rollback()
    return render_template('errors/500.html'), 500
