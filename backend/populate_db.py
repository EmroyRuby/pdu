import os
import random
import django
from datetime import timedelta
from django.utils import timezone
from django.core.files import File

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zpi.settings")
django.setup()

from accounts.models import AppUser
from events.models import Category, Event, EventRegistration, Comment

category_names = [
    "Music", "Technology", "Art", "Sports", "Education",
    "Health & Wellness", "Business", "Food & Drink",
    "Nature", "Fashion", "Literature", "Gaming",
    "Travel", "Science", "Cinema", "Theatre",
    "History", "Photography", "Workshop", "Social"
]
categories = [Category.objects.create(name=name) for name in category_names]

# Creating more realistic events
event_details = [
    {"title": "Summer Music Festival", "description": "An outdoor summer music experience."},
    {"title": "Tech Innovators Conference", "description": "Meet the leading minds in technology."},
    {"title": "Artists' Gallery Night", "description": "A showcase of local and international artists."},
    {"title": "Marathon City Run", "description": "A community running event for all ages."},
    {"title": "Educators' Symposium", "description": "Discussions on the future of education."},
    {"title": "Health and Wellness Expo", "description": "Explore the latest in health and wellness."},
    {"title": "Entrepreneurs' Networking Event", "description": "Connect with fellow business owners."},
    {"title": "International Food Fair", "description": "Taste foods from around the world."},
    # Add more events as needed
]


# Helper function to generate random timezone-aware datetime
def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randint(0, int_delta)
    return start + timedelta(seconds=random_second)


# Creating 25 users
users = []
#for i in range(1, 26):
#    user = AppUser.objects.create_user(email=f'user{i}@example.com', username=f'user{i}', password='password123',
#                                       is_active=True)
#    users.append(user)

# Creating 8 events
events = []
for event in event_details:
    photo_path = f'/var/www/zpi/media/events/event_photo_{random.randint(1, 8)}.jpg'
    with open(photo_path, 'rb') as photo_file:
        photo = File(photo_file, name=os.path.basename(photo_path))
        new_event = Event.objects.create(
            title=event["title"],
            user=random.choice(users),
            description=event["description"],
            location=f'{random.choice(["Downtown", "City Park", "Beachfront", "Convention Center", "Town Hall"])}',
            is_public=random.choice([True, False]),
            price=random.uniform(0, 100),
            capacity=random.randint(50, 500),
            registration_end_date=random_date(timezone.now(), timezone.now() + timedelta(days=30)),
            start_date=timezone.now() + timedelta(days=random.randint(30, 60)),
            end_date=timezone.now() + timedelta(days=random.randint(61, 90)),
            photo=photo
        )
    assigned_categories = random.sample(categories, random.randint(2, 5))
    for category in assigned_categories:
        new_event.categories.add(category)
    events.append(new_event)

for i in range(1, 26):

    # Randomly registering each user for 1-5 events
    registered_events = random.sample(events, random.randint(1, 5))
    for event in registered_events:
        # Check if the user is already registered for the event
        if not EventRegistration.objects.filter(user=user, event=event).exists():
            EventRegistration.objects.create(event=event, user=user)

            # Creating a comment for each event the user is registered for
            Comment.objects.create(user=user, event=event, content=f'Comment by user {i} on Event {event.id}')

print('Database populated with sample data!')
