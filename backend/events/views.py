from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .models import Event, EventNotification, Response, EventRegistration, Category, EventCategory, Comment
from .serializers import (
    EventSerializer, EventNotificationSerializer, ResponseSerializer, EventRegistrationSerializer,
    CategorySerializer, EventCategorySerializer, CommentSerializer
)
from django.http import JsonResponse


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventNotificationViewSet(viewsets.ModelViewSet):
    queryset = EventNotification.objects.all()
    serializer_class = EventNotificationSerializer

class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class EventCategoryViewSet(viewsets.ModelViewSet):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

