import django
django.setup()
from django.contrib.auth.models import User
from events.models import Event, EventNotification, RegistrationResponse, EventRegistration, Category, EventCategory, Comment
from django.utils import timezone
import os

# Set the DJANGO_SETTINGS_MODULE environment variable to point to your project's settings module.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# Initialize Django.

# Now you can import your Django models and run your code.



# Create five User instances
users = []
for i in range(5):
    user = User.objects.create(username=f"user_{i}", password="password123")
    users.append(user)

# Create five Event instances
events = []
for i in range(5):
    event = Event.objects.create(
        title=f"Event {i}",
        organizer_id=users[i],
        description=f"This is event {i} description.",
        location=f"Location {i}",
        is_public=True,
        price=50.00,
        capacity=100,
        registration_end_date=timezone.now() + timezone.timedelta(days=7),
        start_date=timezone.now() + timezone.timedelta(days=10),
        end_date=timezone.now() + timezone.timedelta(days=12),
    )
    events.append(event)

# Create five EventNotification instances
event_notifications = []
for i in range(5):
    event_notification = EventNotification.objects.create(
        event_id=events[i],
        title=f"Notification {i}",
        content=f"This is notification {i} content.",
    )
    event_notifications.append(event_notification)

# Create five Response instances
responses = []
for i in range(5):
    response = RegistrationResponse.objects.create(content=f"Response {i}")
    responses.append(response)

# Create five EventRegistration instances
event_registrations = []
for i in range(5):
    event_registration = EventRegistration.objects.create(
        event_id=events[i],
        user_id=users[i],
        response_id=responses[i],
    )
    event_registrations.append(event_registration)

# Create five Category instances
categories = []
for i in range(5):
    category = Category.objects.create(name=f"Category {i}")
    categories.append(category)

# Create five EventCategory instances
event_categories = []
for i in range(5):
    event_category = EventCategory.objects.create(
        event_id=events[i],
        category_id=categories[i],
    )
    event_categories.append(event_category)

# Create five Comment instances
comments = []
for i in range(5):
    comment = Comment.objects.create(
        user_id=users[i],
        event_id=events[i],
        content=f"Comment {i} on Event {i}.",
    )
    comments.append(comment)