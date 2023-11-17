import os

from django.core.mail import send_mail
from environ import environ

environ.Env.read_env("../../.env")
DELETE_SUBJECT = "Event deleted"
DELETE_CONTENT = "CONTENT FOR EVENT DELETED"

def send_notification(emails, subject, content):
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



