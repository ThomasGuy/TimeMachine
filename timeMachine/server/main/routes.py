import logging

# third party imports
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_user, logout_user, login_required
from flask_sqlalchemy_session import current_session as cs

# third party imports
from . import bp
from ...database.models import User


log = logging.getLogger(__name__)


@bp.route('/')
@bp.route('/index')
def index():
    
    return render_template('main/index.html', title='Ahoy Captain')


@bp.route('/user/<username>')
@login_required
def user(username):
    user = cs.query(User).filter_by(username=username).first_or_404()
    profile = {
        'author' : user
    }
    return render_template('main/user.html', user=user, profile=profile)
