from rest_framework import permissions, viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from .models import (Event, EventNotification, RegistrationResponse,
                     EventRegistration, Category, EventCategory, Comment)
from .serializers import (EventSerializer, EventNotificationSerializer,
                          RegistrationResponseSerializer, EventRegistrationSerializer,
                          CategorySerializer, EventCategorySerializer, CommentSerializer)

from datetime import date


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    filter_params = {}

    def get_queryset(self):
        # If no query parameters have values, return default queryset
        if not self.request.query_params:
            return self.queryset

        # If there are query parameters, but they are invalid
        elif all(self.request.query_params.get(param) is None for param in self.filter_params):
            return self.queryset.none()

        queryset = self.queryset.all()
        query_params = self.request.query_params

        for param, lookup in self.filter_params.items():
            value = query_params.get(param)
            if value:
                if '_date' in param:  # for date fields
                    value = date.fromisoformat(value)
                queryset = queryset.filter(**{lookup: value})

        return queryset


class EventViewSet(BaseViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_params = {
        'id': 'id',
        'title': 'title__iexact',
        'location': 'location__iexact',
        'is_public': 'is_public',
        'category_name': 'eventcategory__category_id__name__iexact',
        'start_date': 'start_date__gte',
        'end_date': 'end_date__lte',
        'price_gte': 'price__gte',
        'price_lte': 'price__lte',
        'organizer_id': 'organizer_id'
    }


class EventNotificationViewSet(BaseViewSet):
    queryset = EventNotification.objects.all()
    serializer_class = EventNotificationSerializer
    filter_params = {
        'id': 'id',
        'event_id': 'event_id',
        'title': 'title__iexact',
        'sent_date_start': 'sent_date__gte',
        'sent_date_end': 'sent_date__lte'
    }


class RegistrationResponseViewSet(BaseViewSet):
    queryset = RegistrationResponse.objects.all()
    serializer_class = RegistrationResponseSerializer
    filter_params = {
        'id': 'id',
        'content': 'content__iexact'
    }


class EventRegistrationViewSet(BaseViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    filter_params = {
        'id': 'id',
        'event_id': 'event_id',
        'user_id': 'user_id',
        'response_id': 'response_id',
        'registration_date_start': 'registration_date__gte',
        'registration_date_end': 'registration_date__lte'
    }


class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_params = {
        'id': 'id',
        'name': 'name__iexact'
    }


class EventCategoryViewSet(BaseViewSet):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    filter_params = {
        'id': 'id',
        'event_id': 'event_id',
        'category_id': 'category_id'
    }

    def list(self, request, *args, **kwargs):
        if 'event_id' in request.query_params:
            queryset = self.filter_queryset(self.get_queryset())
            category_names = [event_category.category_id.name for event_category in queryset]
            return Response(category_names, status=status.HTTP_200_OK)
        return super(EventCategoryViewSet, self).list(request, *args, **kwargs)


class CommentViewSet(BaseViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_params = {
        'id': 'id',
        'user_id': 'user_id',
        'event_id': 'event_id',
        'content': 'content__iexact'
    }