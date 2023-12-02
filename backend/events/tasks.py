# events/tasks.py
import logging
from smtplib import SMTPServerDisconnected

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from events.mailing_system import send_notification
from events.models import Event, EventRegistration, GuestRegistration

logger = logging.getLogger(__name__)  # Set up logging


@shared_task
def send_event_notifications():

    try:
        current_time = timezone.now()
        upcoming_events = Event.objects.filter(
            start_date__range=(current_time, current_time + timezone.timedelta(hours=24))
        )

        for event in upcoming_events:
            registered_users = EventRegistration.objects.filter(
                event=event,
                is_registered=True
            ).select_related('user')

            guest_emails = list(GuestRegistration.objects.filter(event=event, verified=True).values_list('email', flat=True))

            emails = [registration.user.email for registration in registered_users]
            emails = emails + guest_emails
            send_notification(emails, f'Upcoming Event: {event.title}', f'Reminder: The event "{event.title}" is starting soon!')
    except SMTPServerDisconnected as e:
        logger.error(f"Failed to send email: {e}")


@shared_task
def send_verification_email(email, verification_code, event_id=None, user_id=None, retry_count=0):
    # Construct the email verification link

    if event_id is None:
        verification_link = f"http://127.0.0.1:8000/api/accounts/verify-registration?code={verification_code}&user_id={user_id}"
    else:
        verification_link = f"http://127.0.0.1:8000/verify-guest-registration?code={verification_code}&event_id={event_id}"
    # Send the email (you can use your preferred email backend)
    try:
        send_mail(
            'Verify Your Event Registration',
            f'Please click the following link to verify your email and complete the registration: {verification_link}',
            'from@example.com',
            [email],
            fail_silently=False,
        )
    except SMTPServerDisconnected as e:
        logger.error(f"Failed to send email: {e}")
        if retry_count < 3:  # Retry up to 3 times
            send_verification_email(email, verification_code, event_id, retry_count + 1)
        else:
            logger.error("Max retries reached for sending email.")
            # Optionally, inform the user or take additional actions


