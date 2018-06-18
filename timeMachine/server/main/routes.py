import logging

# third party imports
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_user, logout_user, login_required

# third party imports
from . import bp
# from timeMachine import session as db


log = logging.getLogger(__name__)


@bp.route('/')
@bp.route('/index')
def index():
    user= {'username': 'Sporty'}
    return render_template('main/index.html', title='Ahoy Captain', user=user)
