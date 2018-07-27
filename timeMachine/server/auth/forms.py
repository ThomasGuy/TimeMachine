import logging

# third party imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from flask_sqlalchemy_session import current_session

# package imports
from timeMachine.database.models import User


log = logging.getLogger(__name__)


class LoginForm(FlaskForm):
    """login"""
    username = StringField('Userneame', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """Registration"""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = current_session.query(User).filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = current_session.query(User).filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


# class ResetPasswordRequestForm(FlaskForm):
#     email = StringField(_l('Email'), validators=[DataRequired(), Email()])
#     submit = SubmitField(_l('Request Password Reset'))


# class ResetPasswordForm(FlaskForm):
#     password = PasswordField(_l('Password'), validators=[DataRequired()])
#     password2 = PasswordField(
#         _l('Repeat Password'), validators=[DataRequired(),
#                                            EqualTo('password')])
#     submit = SubmitField(_l('Request Password Reset'))
