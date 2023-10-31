import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zpi.settings")
import django
django.setup()

from events.models import Event, EventNotification, RegistrationResponse, EventRegistration, Category, EventCategory, \
    Comment
from django.utils import timezone
from accounts.models import AppUser
import random
from faker import Faker

# Set the DJANGO_SETTINGS_MODULE environment variable to point to your project's settings module.

fake = Faker()


# Helper function to create a random user
def create_user():
    email = fake.email()
    password = "password123"
    username = fake.user_name()
    user = AppUser.objects.create_user(email=email, password=password, username=username)
    return user


# Helper function to create a random event
def create_event(organizer):
    title = fake.sentence()
    description = fake.text()
    location = fake.city()
    is_public = random.choice([True, False])
    price = random.uniform(0, 500)  # random price between 0 and 500
    capacity = random.randint(0, 1000)
    days_ahead = random.randint(1, 365)
    start_date = timezone.now() + timezone.timedelta(days=days_ahead)
    end_date = start_date + timezone.timedelta(hours=random.randint(1, 72))  # random duration between 1 and 72 hours
    event = Event.objects.create(
        title=title, user_id=organizer, description=description, location=location,
        is_public=is_public, price=price, capacity=capacity, registration_end_date=start_date,
        start_date=start_date, end_date=end_date)
    return event


# Create a specified number of users
num_users = 10  # specify the number of users you want to create
users = [create_user() for _ in range(num_users)]

# Create events for users
num_events_per_user = 5
events = []
for user in users:
    events.extend(create_event(user) for _ in range(num_events_per_user))

# Create other entities related to events
for event in events:
    # Create EventNotification
    title = fake.sentence()
    content = fake.text()
    EventNotification.objects.create(event_id=event, title=title, content=content)

    # Create EventRegistration and RegistrationResponse
    user = random.choice(users)  # select a random user
    response = RegistrationResponse.objects.create(content=fake.sentence()[0:45])
    EventRegistration.objects.create(event_id=event, user_id=user, response_id=response)

    # Create Categories and associate them with events
    category, created = Category.objects.get_or_create(name=fake.word())  # This avoids category duplication
    EventCategory.objects.create(event_id=event, category_id=category)

    # Create Comments on events
    content = fake.text()
    Comment.objects.create(user_id=user, event_id=event, content=content)
