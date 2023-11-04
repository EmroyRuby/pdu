import os

from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zpi.settings")
import django
django.setup()

from events.models import Event, EventNotification, EventRegistration, Category, Comment
from accounts.models import AppUser
import random
from faker import Faker

fake = Faker()

# Deleting all data
Comment.objects.all().delete()
EventRegistration.objects.all().delete()
EventNotification.objects.all().delete()
Event.objects.all().delete()
Category.objects.all().delete()
AppUser.objects.all().delete()


def create_user():
    email = fake.email()
    password = "password123"
    username = fake.user_name()
    user = AppUser.objects.create_user(email=email, password=password, username=username)
    return user


def create_event(organizer):
    title = fake.sentence()
    description = fake.text()
    location = fake.city()
    is_public = random.choice([True, False])
    price = random.uniform(0, 500)
    capacity = random.randint(0, 1000)
    days_ahead = random.randint(1, 365)
    start_date = timezone.now() + timezone.timedelta(days=days_ahead)
    end_date = start_date + timezone.timedelta(hours=random.randint(1, 72))
    event = Event.objects.create(
        title=title, user=organizer, description=description, location=location,
        is_public=is_public, price=price, capacity=capacity, registration_end_date=start_date,
        start_date=start_date, end_date=end_date)

    # Create Categories and associate them with events
    category, created = Category.objects.get_or_create(name=fake.word())
    event.categories.add(category)

    return event


num_users = 10
users = [create_user() for _ in range(num_users)]

num_events_per_user = 5
events = []
for user in users:
    events.extend(create_event(user) for _ in range(num_events_per_user))

for event in events:
    title = fake.sentence()
    content = fake.text()
    EventNotification.objects.create(event=event, title=title, content=content)

    user = random.choice(users)
    is_registered = True
    EventRegistration.objects.create(event=event, user=user, is_registered=is_registered)

    content = fake.text()
    Comment.objects.create(user=user, event=event, content=content)
