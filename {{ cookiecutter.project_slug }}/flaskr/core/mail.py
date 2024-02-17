from flask_mail import Message

from flaskr.core import prod_settings
from flaskr.extensions import mail


def send_email(to: str, subject: str, template: str):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=prod_settings.MAIL_DEFAULT_SENDER,
    )
    mail.send(msg)
