from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=70)
    organizer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    location = models.CharField(max_length=255)
    is_public = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    capacity = models.PositiveIntegerField(null=True)
    registration_end_date = models.DateTimeField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EventNotification(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    title = models.CharField(max_length=70)
    content = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)


class Response(models.Model):
    content = models.CharField(max_length=50)

class EventRegistration(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    response_id = models.ForeignKey(Response, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    name = models.CharField(max_length=70)

class EventCategory(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)



