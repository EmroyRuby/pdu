from django.db import models

from accounts.models import AppUser


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=70)
    objects = models.Manager()


class Event(models.Model):
    title = models.CharField(max_length=70)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
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
    photo = models.ImageField(upload_to='events', null=True)
    categories = models.ManyToManyField(Category)
    objects = models.Manager()


class EventNotification(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    title = models.CharField(max_length=70)
    content = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    is_registered = models.BooleanField(default=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        unique_together = ('user', 'event')  # This ensures that the combination of user and event is unique


class Comment(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    objects = models.Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)