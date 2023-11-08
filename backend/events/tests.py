# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Category, Event, EventNotification, EventRegistration, Comment

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from datetime import datetime

from .models import Event, EventNotification, EventRegistration, Category, Comment

User = get_user_model()


class ModelsTests(TestCase):
    def test_category_model(self):
        category = Category(name="Test Category")
        category.save()

        self.assertEqual(category.name, "Test Category")

    def test_event_model(self):
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword'
        )
        event = Event(
            title="Test Event",
            user=user,
            description="Test description",
            location="Test location",
            is_public=True,
            price=25.0,
            capacity=100,
            registration_end_date="2023-01-01T00:00:00Z",
            start_date="2023-01-02T00:00:00Z",
            end_date="2023-01-03T00:00:00Z"
        )
        event.save()

        self.assertEqual(event.title, "Test Event")
        self.assertEqual(event.user, user)

    def test_event_notification_model(self):
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword'
        )
        event = Event(
            title="Test Event",
            user=user,
            description="Test description",
            location="Test location",
            is_public=True,
            price=25.0,
            capacity=100,
            registration_end_date="2023-01-01T00:00:00Z",  # Provide a valid date and time
            start_date="2023-01-02T00:00:00Z",
            end_date="2023-01-03T00:00:00Z"
        )
        event.save()
        notification = EventNotification(event=event, title="Test Notification", content="Test content")
        notification.save()

        self.assertEqual(notification.title, "Test Notification")
        self.assertEqual(notification.content, "Test content")
        self.assertEqual(notification.event, event)

    def test_event_registration_model(self):
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword'
        )
        event = Event(
            title="Test Event",
            user=user,
            description="Test description",
            location="Test location",
            is_public=True,
            price=25.0,
            capacity=100,
            registration_end_date="2023-01-01T00:00:00Z",  # Provide a valid date and time
            start_date="2023-01-02T00:00:00Z",
            end_date="2023-01-03T00:00:00Z"
        )
        event.save()
        registration = EventRegistration(event=event, user=user, is_registered=True)
        registration.save()

        self.assertEqual(registration.user, user)
        self.assertEqual(registration.event, event)
        self.assertTrue(registration.is_registered)

    def test_comment_model(self):
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword'
        )
        event = Event(
            title="Test Event",
            user=user,
            description="Test description",
            location="Test location",
            is_public=True,
            price=25.0,
            capacity=100,
            registration_end_date="2023-01-01T00:00:00Z",  # Provide a valid date and time
            start_date="2023-01-02T00:00:00Z",
            end_date="2023-01-03T00:00:00Z"
        )
        event.save()

        comment = Comment(user=user, event=event, content="Test comment")
        comment.save()

        self.assertEqual(comment.user, user)
        self.assertEqual(comment.event, event)
        self.assertEqual(comment.content, "Test comment")

    # Add more test cases for other view functions in EventViewSet


class EventNotificationViewSetTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_event_notification(self):
        # Create an event first (similar to the previous test)
        # Then create an event notification associated with that event
        event = Event.objects.create(title='Test Event', user=self.user, description='Event description', location='Event location', is_public=True, price='25.00', capacity=100, registration_end_date=datetime.now(), start_date=datetime.now(), end_date=datetime.now())
        url = reverse('eventnotification-list')
        data = {
            'event': event.id,
            'title': 'Test Notification',
            'content': 'Notification content',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Add more test cases for other view functions in EventNotificationViewSet


class CategoryViewSetTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_category(self):
        url = reverse('category-list')
        data = {
            'name': 'Test Category',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Add more test cases for other view functions in CategoryViewSet



