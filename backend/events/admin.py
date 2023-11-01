from django.contrib import admin

from .models import AppUser, Event, EventNotification, RegistrationResponse, EventRegistration, Category, EventCategory, \
    Comment

# Register your models here.

# Registering the models with basic functionality
admin.site.register(AppUser)
admin.site.register(Event)
admin.site.register(EventNotification)
admin.site.register(RegistrationResponse)
admin.site.register(EventRegistration)
admin.site.register(Category)
admin.site.register(EventCategory)
admin.site.register(Comment)
