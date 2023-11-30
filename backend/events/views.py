from datetime import date

from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from events.mailing_system import send_notification, DELETE_CONTENT, DELETE_SUBJECT
from .models import (Event, EventNotification,
                     EventRegistration, Category, Comment, GuestRegistration)
from .my_permissions import IsOwnerOrReadOnlyOrSuperuser, CanViewAndPostOnly
from .serializers import (EventSerializer, EventNotificationSerializer,
                          EventRegistrationSerializer,
                          CategorySerializer, CommentSerializer, GuestRegistrationSerializer)
import logging
from .recommendation_model import get_recommendations

logger = logging.getLogger('events')


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnlyOrSuperuser]
    authentication_classes = [SessionAuthentication]

    filter_params = {}

    def get_queryset(self):
        # If no query parameters have values, return default queryset
        if not self.request.query_params:
            queryset = super().get_queryset()
            return queryset.all()

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
    permission_classes = [IsOwnerOrReadOnlyOrSuperuser]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_params = {
        'id': 'id',
        'title': 'title__icontains',
        'location': 'location__icontains',
        'is_public': 'is_public',
        'category': 'categories__name__in',
        'start_date': 'start_date__gte',
        'end_date': 'end_date__lte',
        'price_gte': 'price__gte',
        'price_lte': 'price__lte',
        'user': 'user'
    }

    # to associate event with current user id
    def perform_create(self, serializer):
        # Set the user to the current user
        serializer.save(user=self.request.user)
        logger.info(f"Event created with title '{serializer.instance.title}' by user {self.request.user.user_id}")

    def destroy(self, request, *args, **kwargs):
        event = self.get_object()  # This will use the queryset to get the object, which already accounts for permissions.

        # Check if the user is allowed to delete this event
        if not (event.user == request.user or request.user.is_superuser):
            raise PermissionDenied("You do not have permission to delete this event.")

        # regular user emails registered for event
        registered_emails = list(EventRegistration.objects.filter(event=event)
                                 .values_list('user__email', flat=True))

        # add guest registrations to required email list
        registered_emails += GuestRegistration.objects.filter(event=event, verified=True).values_list('email',
                                                                                                      flat=True)
        logger.info(f"Registered emails for event {event.id}: {registered_emails}")
        send_notification(emails=registered_emails, subject=DELETE_SUBJECT, content=DELETE_CONTENT)
        logger.info(f"Notification sent for event {event.id} with subject '{DELETE_SUBJECT}'.")

        # Perform the deletion
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        event = self.get_object()
        # Store original values before they are updated
        original_start_date = event.start_date
        original_end_date = event.end_date
        original_location = event.location

        serializer = self.get_serializer(event, data=request.data, partial=kwargs.pop('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # After updating, check if the specific fields have changed
        if (event.start_date != original_start_date or
                event.end_date != original_end_date or
                event.location != original_location):

            # Prepare a message to notify users of the change
            message = "The details of event '{}' have changed.".format(event.title)
            if event.start_date != original_start_date:
                message += "\nNew start date: {}".format(event.start_date)
            if event.end_date != original_end_date:
                message += "\nNew end date: {}".format(event.end_date)
            if event.location != original_location:
                message += "\nNew location: {}".format(event.location)

            # regular user emails registered for event
            registered_emails = list(EventRegistration.objects.filter(event=event)
                                     .values_list('user__email', flat=True))

            # add guest registrations to required email list
            registered_emails += GuestRegistration.objects.filter(event=event, verified=True).values_list('email',
                                                                                                          flat=True)
            logger.info(f"Sending update notification for event {event.id} to emails: {registered_emails}")
            send_notification(emails=registered_emails, subject="Event Update Notification", content=message)

        return Response(serializer.data)


class EventNotificationViewSet(BaseViewSet):
    permission_classes = [CanViewAndPostOnly]
    queryset = EventNotification.objects.all()
    serializer_class = EventNotificationSerializer
    filter_params = {
        'id': 'id',
        'title': 'title__iexact',
        'sent_date_start': 'sent_date__gte',
        'sent_date_end': 'sent_date__lte'
    }

    def create(self, request, *args, **kwargs):
        event_id = request.data.get('event')
        event = Event.objects.filter(pk=event_id, user=request.user).first()
        if not event:
            return Response(
                {"detail": "You do not have permission to add notifications for this event."},
                status=status.HTTP_403_FORBIDDEN
            )

        # regular user emails registered for event
        registered_emails = list(EventRegistration.objects.filter(event=event_id)
                                 .values_list('user__email', flat=True))

        # add guest registrations to required email list
        registered_emails += GuestRegistration.objects.filter(event=event, verified=True).values_list('email',
                                                                                                      flat=True)

        logger.info(f"Registered emails for event {event_id}: {registered_emails}")
        send_notification(emails=registered_emails, subject=request.data['title'], content=request.data['content'])
        logger.info(f"Notification sent for event {event_id} with subject '{request.data['title']}'.")

        return super().create(request, *args, **kwargs)

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

        # at /api/event-notifications user will see all his notifications
        # at /api/event-notifications?event user will see all notifications for an event, if he's owner of it
        event = query_params.get('event')
        if event:
            try:
                event = Event.objects.get(id=event)
                if event.user == self.request.user:
                    user_notifications = EventNotification.objects.filter(event=event)
                else:
                    # If the user is neither the owner nor a superuser, return an empty queryset
                    return EventNotification.objects.none()
            except Event.DoesNotExist:
                return EventRegistration.objects.none()
        for param, lookup in self.filter_params.items():
            value = query_params.get(param)
            if value:
                if '_date' in param:  # for date fields
                    value = date.fromisoformat(value)
                user_notifications = user_notifications.filter(**{lookup: value})

        return user_notifications


# at /api/event-registrations user will see his own registrations
# at /api/event-registrations?event=ID user will see all event registrations on his own event
class EventRegistrationViewSet(BaseViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    filter_params = {
        'id': 'id',
        'user': 'user',
        'is_registered': 'is_registered',
        'registration_date_start': 'registration_date__gte',
        'registration_date_end': 'registration_date__lte'
    }

    def create(self, request, *args, **kwargs):
        # Overriding create method to set the user and handle registrations
        user = self.request.user
        event_id = request.data.get('event')
        # Handling the error when the event does not exist
        try:
            event_obj = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"detail": "Event does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is already registered for this event
        if EventRegistration.objects.filter(user=user, event=event_id).exists():
            event_registration = EventRegistration.objects.get(user=user, event=event_id)
            if event_registration.is_registered:
                return Response({"detail": "User is already registered for this event."},
                                status=status.HTTP_400_BAD_REQUEST)
            elif event_obj.capacity == 0:
                return Response({"detail": "All slots are taken"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                event_registration.is_registered = True
                event_registration.save()
                return Response({"detail": "Registered successfully"},
                                status=status.HTTP_201_CREATED)

        # Create the registration
        registration = EventRegistration.objects.create(user=user, event_id=event_id)

        serializer = EventRegistrationSerializer(registration)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        try:
            registration = self.get_object()
        except EventRegistration.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        registration.is_registered = False
        registration.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        query_params = self.request.query_params
        user_registrations = self.queryset.filter(user=self.request.user)

        # if user is superuser return all objects
        if self.request.user.is_superuser:
            return EventRegistration.objects.all()

        # when querying for specific event
        event = query_params.get('event')
        if event:
            try:
                event = Event.objects.get(id=event)
                if event.user == self.request.user:
                    user_registrations = EventRegistration.objects.filter(event=event)
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
    permission_classes = [CanViewAndPostOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_params = {
        'id': 'id',
        'name': 'name__iexact'
    }

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        if Category.objects.filter(name=name).exists():
            return Response({"detail": "This category already exist"}, status=status.HTTP_409_CONFLICT)
        else:
            category = Category.objects.create(name=name)
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentViewSet(BaseViewSet):
    permission_classes = [CanViewAndPostOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_params = {
        'id': 'id',
        'user': 'user',
        'event': 'event',
        'content': 'content__iexact'
    }

    def create(self, request, *args, **kwargs):
        # Get the event ID from the request data
        event_id = request.data.get('event')

        # Ensure the event ID is provided
        if not event_id:
            return Response({"detail": "Event ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Ensure the event exists
            event = Event.objects.get(pk=event_id)

            # # Check if the event has already ended
            # if timezone.now() <= event.end_date:
            #     return Response({"detail": "Can't comment on an event that hasn't ended."},
            #                     status=status.HTTP_400_BAD_REQUEST)
            #
            # # Check if the user is registered for the event
            # if not EventRegistration.objects.filter(user=request.user, event=event, is_registered=True).exists():
            #     return Response({"detail": "You must be registered for the event to comment."},
            #                     status=status.HTTP_403_FORBIDDEN)
            #
            # # Check if the user has already commented on the event
            # if Comment.objects.filter(user=request.user, event=event).exists():
            #     return Response({"detail": "You can only comment once on an event."},
            #                     status=status.HTTP_400_BAD_REQUEST)

            # Create the comment
            comment_serializer = self.get_serializer(data=request.data)
            comment_serializer.is_valid(raise_exception=True)
            comment_serializer.save(user=request.user, event=event)

            return Response(comment_serializer.data, status=status.HTTP_201_CREATED)

        except Event.DoesNotExist:
            return Response({"detail": "Event does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Handle other possible exceptions
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GuestRegistrationAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [SessionAuthentication]

    @swagger_auto_schema(
        operation_description="Register a guest user by email.",
        request_body=GuestRegistrationSerializer,
        responses={
            status.HTTP_201_CREATED: '{"message": "Please check your email to confirm registration."}',
            status.HTTP_400_BAD_REQUEST: 'Bad Request',
        },
        tags=['Guest Registration'],
    )
    def post(self, request, *args, **kwargs):
        serializer = GuestRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            event = serializer.validated_data['event']

            # Check if the event is public
            if not event.is_public:
                return Response(
                    {"detail": "Only public events are open for guest registration."},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Check if the email is already registered for the event among users
            if EventRegistration.objects.filter(event=event, user__email=email).exists():
                raise ValidationError('This email is already registered for the event.')

            # Check if the email is already registered for the event among guests
            if GuestRegistration.objects.filter(event=event, email=email, verified=True).exists():
                raise ValidationError('This email is already registered for the event as a guest.')

            # Save the new guest registration
            serializer.save()
            # You might want to send a response with further instructions
            return Response(
                {"message": "Please check your email to confirm registration."},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyGuestRegistration(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [SessionAuthentication]

    def get(self, request, *args, **kwargs):
        # Retrieve verification code and event_id from the request's query parameters
        verification_code = request.query_params.get('code')
        event_id = request.query_params.get('event_id')

        if not verification_code or not event_id:
            return Response({"detail": "Missing verification code or event ID."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the guest registration using the verification code and event_id
            guest_registration = GuestRegistration.objects.get(
                verification_code=verification_code,
                event_id=event_id,
                verified=False  # Assuming you have an 'verified' field to check if it's already verified
            )
        except GuestRegistration.DoesNotExist:
            return Response({"detail": "Invalid verification code or event ID, or already verified."},
                            status=status.HTTP_404_NOT_FOUND)

        # If the registration exists and is not verified, verify it
        guest_registration.verified = True
        guest_registration.save()

        # After verification, you might want to redirect the user or send a success response
        return Response({"message": "Email verified successfully. You are now registered for the event."},
                        status=status.HTTP_200_OK)


class UserRecommendation(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    filter_params = {
        'id': 'id',
        'title': 'title__icontains',
        'location': 'location__icontains',
        'is_public': 'is_public',
        'category': 'categories__name__in',
        'start_date': 'start_date__gte',
        'end_date': 'end_date__lte',
        'price_gte': 'price__gte',
        'price_lte': 'price__lte',
        'user': 'user'
    }

    def get(self, request, *args, **kwargs):
        try:
            # Retrieve the logged-in user's email
            user_email = request.user.email
            recommended_events_id = get_recommendations(user_email)

            # Fetch the recommended events from the database
            recommended_events = Event.objects.filter(id__in=recommended_events_id)

            # Apply additional filtering based on query parameters
            recommended_events = self.apply_filtering(recommended_events, request.query_params)

            # Serialize the event data
            serializer = EventSerializer(recommended_events, many=True)
            return Response(serializer.data)

        except Event.DoesNotExist:
            # Handle the case where the Event does not exist
            return Response({'error': 'Events not found.'}, status=status.HTTP_404_NOT_FOUND)

    def apply_filtering(self, queryset, query_params):
        if all(query_params.get(param) is None for param in self.filter_params):
            return queryset

        for param, lookup in self.filter_params.items():
            value = query_params.get(param)
            if value:
                if param == 'category':  # Special handling for categories
                    value = value.split(',')
                elif '_date' in param:  # for date fields
                    value = date.fromisoformat(value)
                queryset = queryset.filter(**{lookup: value})
        return queryset

