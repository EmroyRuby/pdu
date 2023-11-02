from datetime import date

from rest_framework import permissions, viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from .models import (Event, EventNotification, RegistrationResponse,
                     EventRegistration, Category, EventCategory, Comment)
from .my_permissions import IsOwnerOrReadOnlyOrSuperuser
from .serializers import (EventSerializer, EventNotificationSerializer,
                          RegistrationResponseSerializer, EventRegistrationSerializer,
                          CategorySerializer, EventCategorySerializer, CommentSerializer)


# TODO
# event-registrations - user widzi swoje rejestracje na event
# event-registrations?event - user widzi wszystkie rejestracje innych na swoj event
# filtrowanie po tagach i patternie tytulu
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
                if '_date' in param:  # for date fields
                    value = date.fromisoformat(value)
                queryset = queryset.filter(**{lookup: value})

        return queryset


class EventViewSet(BaseViewSet):

    permission_classes = [permissions.AllowAny, IsOwnerOrReadOnlyOrSuperuser]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_params = {
        'id': 'id',
        'title': 'title__iexact',
        'location': 'location__iexact',
        'is_public': 'is_public',
        'category_name': 'eventcategory__category__name__iexact',
        'start_date': 'start_date__gte',
        'end_date': 'end_date__lte',
        'price_gte': 'price__gte',
        'price_lte': 'price__lte',
        'user': 'user'
    }




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
        # First, filter based on the logged-in user
        if self.request.user.is_superuser:
            user_registrations = self.queryset.all()
        else:
            owned_events_ids = Event.objects.filter(user=self.request.user).values_list(
                'id', flat=True)
            user_registrations = self.queryset.filter(event__in=owned_events_ids)

        # Now apply other filters if any
        query_params = self.request.query_params

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


class EventCategoryViewSet(BaseViewSet):
    permission_classes = [permissions.AllowAny, IsOwnerOrReadOnlyOrSuperuser]
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    filter_params = {
        'id': 'id',
        'event': 'event',
        'category': 'category'
    }

    def list(self, request, *args, **kwargs):
        if 'event' in request.query_params:
            queryset = self.filter_queryset(self.get_queryset())
            category_names = [event_category.category.name for event_category in queryset]
            return Response(category_names, status=status.HTTP_200_OK)
        return super(EventCategoryViewSet, self).list(request, *args, **kwargs)


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
