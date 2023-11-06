from django.contrib import admin

from .models import AppUser, Event, EventNotification, EventRegistration, Category, Comment

# Register your models here.

# Registering the models with basic functionality
admin.site.register(AppUser)
admin.site.register(Event)
admin.site.register(EventNotification)
admin.site.register(EventRegistration)
admin.site.register(Category)
admin.site.register(Comment)
