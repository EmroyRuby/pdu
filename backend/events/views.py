from datetime import date

from rest_framework import permissions, viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from .models import (Event, EventNotification, RegistrationResponse,
                     EventRegistration, Category, Comment)
from .my_permissions import IsOwnerOrReadOnlyOrSuperuser
from .serializers import (EventSerializer, EventNotificationSerializer,
                          RegistrationResponseSerializer, EventRegistrationSerializer,
                          CategorySerializer, CommentSerializer)


# TODO
# dodac usuwanie konta


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnlyOrSuperuser]
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
                if param == 'category':  # Special handling for categories
                    value = value.split(',')
                elif '_date' in param:  # for date fields
                    value = date.fromisoformat(value)
                queryset = queryset.filter(**{lookup: value})
        return queryset


class EventViewSet(BaseViewSet):
    permission_classes = [permissions.AllowAny, IsOwnerOrReadOnlyOrSuperuser]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_params = {
        'id': 'id',
        'title': 'title__icontains',
        'location': 'location__iexact',
        'is_public': 'is_public',
        'category': 'categories__name__in',
        'start_date': 'start_date__gte',
        'end_date': 'end_date__lte',
        'price_gte': 'price__gte',
        'price_lte': 'price__lte',
        'user': 'user',
    }

    #to associate event with current user id
    def perform_create(self, serializer):
        # Set the user to the current user
        serializer.save(user=self.request.user)



class EventNotificationViewSet(BaseViewSet):
    queryset = EventNotification.objects.all()
    serializer_class = EventNotificationSerializer
    filter_params = {
        'id': 'id',
        'event': 'event',
        'title': 'title__iexact',
        'sent_date_start': 'sent_date__gte',
        'sent_date_end': 'sent_date__lte'
    }

    def get_queryset(self):
        # First, filter based on the logged-in user
        if self.request.user.is_superuser:
            user_notifications = self.queryset.all()
        else:
            registered_event_ids = EventRegistration.objects.filter(user=self.request.user).values_list(
                'event', flat=True)
            user_notifications = self.queryset.filter(event__in=registered_event_ids)

        # Now apply other filters if any
        query_params = self.request.query_params

        for param, lookup in self.filter_params.items():
            value = query_params.get(param)
            if value:
                if '_date' in param:  # for date fields
                    value = date.fromisoformat(value)
                user_notifications = user_notifications.filter(**{lookup: value})

        return user_notifications


class RegistrationResponseViewSet(BaseViewSet):
    permission_classes = [permissions.AllowAny, IsOwnerOrReadOnlyOrSuperuser]
    queryset = RegistrationResponse.objects.all()
    serializer_class = RegistrationResponseSerializer
    filter_params = {
        'id': 'id',
        'content': 'content__iexact'
    }

# at /api/event-registrations user will see his own registrations
# at /api/event-registrations?event=ID user will see all event registrations on his own event
class EventRegistrationViewSet(BaseViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    filter_params = {
        'id': 'id',
        'event': 'event',
        'user': 'user',
        'response': 'response',
        'registration_date_start': 'registration_date__gte',
        'registration_date_end': 'registration_date__lte'
    }

    def get_queryset(self):
        query_params = self.request.query_params
        user_registrations = self.queryset.all()

        event_id = query_params.get('event')
        if event_id:
            try:
                event = Event.objects.get(id=event_id)
                if event.user == self.request.user or self.request.user.is_superuser:
                    user_registrations = user_registrations.filter(event=event)
                else:
                    # If the user is neither the owner nor a superuser, return an empty queryset
                    return EventRegistration.objects.none()
            except Event.DoesNotExist:
                return EventRegistration.objects.none()

        # Apply other filters
        for param, lookup in self.filter_params.items():
            value = query_params.get(param)
            if value:
                if '_date' in param:  # for date fields
                    value = date.fromisoformat(value)
                user_registrations = user_registrations.filter(**{lookup: value})

        return user_registrations


class CategoryViewSet(BaseViewSet):
    permission_classes = [permissions.AllowAny, IsOwnerOrReadOnlyOrSuperuser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_params = {
        'id': 'id',
        'name': 'name__iexact'
    }


class CommentViewSet(BaseViewSet):
    permission_classes = [permissions.AllowAny, IsOwnerOrReadOnlyOrSuperuser]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_params = {
        'id': 'id',
        'user': 'user',
        'event': 'event',
        'content': 'content__iexact'
    }
