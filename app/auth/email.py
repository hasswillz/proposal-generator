import smtplib

from flask import url_for, current_app
from flask_mail import Message
from app import mail

def send_password_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                 sender=current_app.config['MAIL_USERNAME'],
                 recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('auth.reset_password', token=token, _external=True)}

If you did not make this request, please ignore this email.
'''
    try:
        mail.send(msg)
    except smtplib.SMTPAuthenticationError:
        current_app.logger.error("SMTP Authentication failed. Check email credentials.")
        raise
