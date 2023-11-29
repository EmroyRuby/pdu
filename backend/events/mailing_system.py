import logging
import os
from smtplib import SMTPServerDisconnected

from django.core.mail import send_mail
from environ import environ

environ.Env.read_env("../../.env")
DELETE_SUBJECT = "Event deleted"
DELETE_CONTENT = "CONTENT FOR EVENT DELETED"
logger = logging.getLogger(__name__)  # Set up logging


def send_notification(emails, subject, content):
    try:
        REQUEST_ATTEMPTS = 5
        EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
        EMAIL_SUBJECT = subject
        EMAIL_CONTENT = content

        send_mail(
            EMAIL_SUBJECT,
            EMAIL_CONTENT,
            EMAIL_SENDER,
            emails,
            fail_silently=False,
        )
    except SMTPServerDisconnected as e:
        logger.error(f"Failed to send email: {e}")
