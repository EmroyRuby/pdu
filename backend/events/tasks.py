# events/tasks.py

from celery import shared_task
from django.utils import timezone
from events.models import Event, EventRegistration
from events.mailing_system import send_notification

@shared_task

def send_event_notifications():
    current_time = timezone.now()
    upcoming_events = Event.objects.filter(
        start_date__range=(current_time, current_time + timezone.timedelta(hours=24))
    )

    for event in upcoming_events:
        registered_users = EventRegistration.objects.filter(
            event=event,
            is_registered=True
        ).select_related('user')

        emails = [registration.user.email for registration in registered_users]
        send_notification(emails, f'Upcoming Event: {event.title}', f'Reminder: The event "{event.title}" is starting soon!')