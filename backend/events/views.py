# Create your views here.
from rest_framework import permissions
from rest_framework import viewsets
from .models import Event, EventNotification, RegistrationResponse, EventRegistration, Category, EventCategory, Comment
from .serializers import (
    EventSerializer, EventNotificationSerializer, RegistrationResponseSerializer, EventRegistrationSerializer,
    CategorySerializer, EventCategorySerializer, CommentSerializer
)
from datetime import date


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

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
            'title', 'location', 'is_public', 'category_name', 'start_date', 'end_date',
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
        title = self.request.query_params.get('title')
        location = self.request.query_params.get('location')
        is_public = self.request.query_params.get('is_public')
        category_name = self.request.query_params.get('category_name')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        price_lte = self.request.query_params.get('price_lte')
        price_gte = self.request.query_params.get('price_gte')
        organizer_id = self.request.query_params.get('organizer_id')

        # If a category name is provided in the query parameters, filter events by that category
        # iexact - case-insensitive check
        if category_name:
            queryset = queryset.filter(eventcategory__category_id__name=category_name)
        if title:
            queryset = queryset.filter(title__iexact=title)
        if is_public:
            queryset = queryset.filter(is_public=is_public)
        if location:
            queryset = queryset.filter(title__iexact=location)
        if price_gte:
            queryset = queryset.filter(price__gte=price_gte)
        if price_lte:
            queryset = queryset.filter(price__lte=price_lte)
        if organizer_id:
            queryset = queryset.filter(organizer_id=organizer_id)
        # parameter format YYYY-MM-DD
        if start_date:
            start_date = date.fromisoformat(start_date)
            queryset = queryset.filter(start_date__gte=start_date)
        if end_date:
            end_date = date.fromisoformat(end_date)
            queryset = queryset.filter(end_date__lte=end_date)

        return queryset


class EventNotificationViewSet(viewsets.ModelViewSet):
    queryset = EventNotification.objects.all()
    serializer_class = EventNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = RegistrationResponse.objects.all()
    serializer_class = RegistrationResponseSerializer
    permission_classes = [permissions.IsAuthenticated]


class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class EventCategoryViewSet(viewsets.ModelViewSet):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
