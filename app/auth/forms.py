# app/auth/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User
from flask_babel import lazy_gettext as _

class LoginForm(FlaskForm):
    email = StringField(_('Email'), validators=[
        DataRequired(),
        Email(message=_("Please enter a valid email address"))
    ])
    password = PasswordField(_('Password'), validators=[
        DataRequired(),
        Length(min=8, message=_("Password must be at least 8 characters"))
    ])
    remember = BooleanField(_('Remember Me'))
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField(_('Username'), validators=[
        DataRequired(),
        Length(min=4, max=25)
    ])
    email = StringField(_('Email'), validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField(_('Password'), validators=[
        DataRequired(),
        Length(min=8)
    ])
    confirm_password = PasswordField(_('Confirm Password'), validators=[
        DataRequired(),
        EqualTo('password', message=(_('Passwords must match')))
    ])
    submit = SubmitField(_('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(_('Username already taken. Please choose a different one.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(_('Email already registered. Please use a different one.'))

#Password reset na forgot
class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_('Request Password Reset'))

class ResetPasswordForm(FlaskForm):
    password = PasswordField(_('Password'), validators=[DataRequired()])
    password2 = PasswordField(_('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_('Reset Password'))

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(_('Current Password'), validators=[DataRequired()])
    new_password = PasswordField(_('New Password'), validators=[
        DataRequired(),
        Length(min=8, message=_('Password must be at least 8 characters'))
    ])
    confirm_password = PasswordField(_('Confirm New Password'), validators=[
        DataRequired(),
        EqualTo('new_password', message=_('Passwords must match'))
    ])
    submit = SubmitField(_('Change Password'))