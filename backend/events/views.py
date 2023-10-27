# Create your views here.
from rest_framework import permissions, viewsets
from rest_framework.authentication import SessionAuthentication
from .models import Event, EventNotification, RegistrationResponse, EventRegistration, Category, EventCategory, Comment
from .serializers import (
    EventSerializer, EventNotificationSerializer, RegistrationResponseSerializer, EventRegistrationSerializer,
    CategorySerializer, EventCategorySerializer, CommentSerializer
)
from datetime import date


# TODO
#  prevent duplicates in some entities
#  user authentication,
#  api for signup and login

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    # to prevent duplicates
    # def create(self, request, *args, **kwargs):
    #     try:
    #         event = Event.objects.get(title=request.data["title"])
    #         # you can return success like
    #         serialized_data = self.serializer_class(instance=event)
    #         return Response(serialized_data.data, status=status.HTTP_409_CONFLICT)
    #     except ObjectDoesNotExist:
    #         pass
    #     return super().create(request, *args, **kwargs)

    def get_queryset(self):
        # Retrieve the category parameter from the query string (e.g., /events/?category=category_name)
        query_parameters = [
            'id', 'title', 'location', 'is_public', 'category_name', 'start_date', 'end_date',
            'price_gte', 'price_lte', 'organizer_id'
        ]
        # If no query parameters have values, return all objects
        if not self.request.query_params:
            return Event.objects.all()
        # If there are query parameters, but they are invalid
        elif all(self.request.query_params.get(parameter) is None for parameter in query_parameters):
            return Event.objects.none()

        # Start with all events
        queryset = Event.objects.all()
        query_params = self.request.query_params
        # define what filter should be applied to each query parameter
        filter_params = {
            'id': 'id',
            'category_name': 'eventcategory__category_id__name__iexact',
            'title': 'title__iexact',
            'is_public': 'is_public',
            'location': 'location__iexact',
            'price_gte': 'price__gte',
            'price_lte': 'price__lte',
            'organizer_id': 'organizer_id',
            'start_date': 'start_date__gte',
            'end_date': 'end_date__lte'
        }

        for param, lookup in filter_params.items():
            value = query_params.get(param)
            if value:
                if param in ['start_date', 'end_date']:
                    value = date.fromisoformat(value)
                queryset = queryset.filter(**{lookup: value})

        return queryset


class EventNotificationViewSet(viewsets.ModelViewSet):
    queryset = EventNotification.objects.all()
    serializer_class = EventNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        query_parameters = ['id', 'event_id', 'title', 'sent_date_start', 'sent_date_end']

        # If no query parameters have values, return all objects
        if not self.request.query_params:
            return EventNotification.objects.all()
        # If there are query parameters, but they are invalid
        elif all(self.request.query_params.get(parameter) is None for parameter in query_parameters):
            return EventNotification.objects.none()

        filter_params = {
            'id': 'id',
            'event_id': 'event_id',
            'title': 'title__iexact',
            'sent_date_start': 'sent_date__gte',
            'sent_date_end': 'sent_date__lte'
        }
        queryset = EventNotification.objects.all()
        query_params = self.request.query_params
        for param, lookup in filter_params.items():
            value = query_params.get(param)
            if value:
                if param in ['sent_date_start', 'sent_date_end']:
                    value = date.fromisoformat(value)
                queryset = queryset.filter(**{lookup: value})

        return queryset


class RegistrationResponseViewSet(viewsets.ModelViewSet):
    queryset = RegistrationResponse.objects.all()
    serializer_class = RegistrationResponseSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        query_parameters = ['id', 'content']

        # If no query parameters have values, return all objects
        if not self.request.query_params:
            return RegistrationResponse.objects.all()
        # If there are query parameters, but they are invalid
        elif all(self.request.query_params.get(parameter) is None for parameter in query_parameters):
            return RegistrationResponse.objects.none()

        filter_params = {
            'id': 'id',
            'content': 'content__iexact',
        }
        queryset = RegistrationResponse.objects.all()
        query_params = self.request.query_params
        for param, lookup in filter_params.items():
            value = query_params.get(param)
            if value:
                queryset = queryset.filter(**{lookup: value})

        return queryset


class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        query_parameters = ['id', 'event_id', 'user_id', 'response_id', 'registration_date_start',
                            'registration_date_end']

        # If no query parameters have values, return all objects
        if not self.request.query_params:
            return EventRegistration.objects.all()
        # If there are query parameters, but they are invalid
        elif all(self.request.query_params.get(parameter) is None for parameter in query_parameters):
            return EventRegistration.objects.none()

        filter_params = {
            'id': 'id',
            'event_id': 'event_id',
            'user_id': 'user_id',
            'response_id': 'response_id',
            'registration_date_start': 'registration_date__gte',
            'registration_date_end': 'registration_date__lte'
        }
        queryset = EventRegistration.objects.all()
        query_params = self.request.query_params
        for param, lookup in filter_params.items():
            value = query_params.get(param)
            if value:
                if param in ['registration_date_start', 'registration_date_end']:
                    value = date.fromisoformat(value)
                queryset = queryset.filter(**{lookup: value})

        return queryset


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        query_parameters = ['id', 'name']

        # If no query parameters have values, return all objects
        if not self.request.query_params:
            return Category.objects.all()
        # If there are query parameters, but they are invalid
        elif all(self.request.query_params.get(parameter) is None for parameter in query_parameters):
            return Category.objects.none()

        filter_params = {
            'id': 'id',
            'name': 'name__iexact',
        }
        queryset = Category.objects.all()
        query_params = self.request.query_params
        for param, lookup in filter_params.items():
            value = query_params.get(param)
            if value:
                queryset = queryset.filter(**{lookup: value})

        return queryset


class EventCategoryViewSet(viewsets.ModelViewSet):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        query_parameters = ['id', 'event_id', 'category_id']

        # If no query parameters have values, return all objects
        if not self.request.query_params:
            return EventCategory.objects.all()
        # If there are query parameters, but they are invalid
        elif all(self.request.query_params.get(parameter) is None for parameter in query_parameters):
            return EventCategory.objects.none()

        filter_params = {
            'id': 'id',
            'event_id': 'event_id',
            'category_id': 'category_id'
        }
        queryset = EventCategory.objects.all()
        query_params = self.request.query_params
        for param, lookup in filter_params.items():
            value = query_params.get(param)
            if value:
                queryset = queryset.filter(**{lookup: value})

        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        query_parameters = ['id', 'user_id', 'event_id', 'content']

        # If no query parameters have values, return all objects
        if not self.request.query_params:
            return Comment.objects.all()
        # If there are query parameters, but they are invalid
        elif all(self.request.query_params.get(parameter) is None for parameter in query_parameters):
            return Comment.objects.none()

        filter_params = {
            'id': 'id',
            'user_id': 'user_id',
            'event_id': 'event_id',
            'content': 'content__iexact'
        }
        queryset = Comment.objects.all()
        query_params = self.request.query_params
        for param, lookup in filter_params.items():
            value = query_params.get(param)
            if value:
                queryset = queryset.filter(**{lookup: value})

        return queryset
