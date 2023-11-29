import uuid

from rest_framework import serializers

from accounts.models import AppUser
from .models import Event, EventNotification, EventRegistration, Category, Comment, GuestRegistration
from .tasks import send_verification_email


class EventSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Category.objects.all(),
        required=False
    )
    user_email = serializers.SerializerMethodField()
    remaining_slots = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'location', 'is_public', 'price', 'capacity', 'remaining_slots',
                  'registration_end_date', 'start_date', 'end_date', 'created_at', 'updated_at',
                  'user', 'user_email', 'categories', 'photo')
        read_only_fields = ('user', 'user_email',)  # setting user as read-only

    def get_user_email(self, obj):
        user = AppUser.objects.get(user_id=obj.user_id)
        return user.email

    def get_remaining_slots(self, obj):
        if obj.capacity is not None:
            registrations = EventRegistration.objects.filter(event_id=obj.id, is_registered=True)
            return obj.capacity - len(registrations)
        else:
            return None


class EventNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventNotification
        fields = '__all__'


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ('id', 'event', 'event_detail', 'is_registered', 'user_email'
                  , 'registration_date', 'updated_at')

    user_email = serializers.SerializerMethodField(read_only=True)
    event_detail = EventSerializer(source='event', read_only=True)

    def get_user_email(self, obj):
        user = AppUser.objects.get(user_id=obj.user_id)
        return user.email


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'id')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CategoryNameListSerializer(serializers.Serializer):
    name = serializers.CharField()


class GuestRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestRegistration
        fields = ['email', 'event']

    def create(self, validated_data):
        # Create a verification code
        verification_code = uuid.uuid4().hex
        # Create GuestRegistration object with verification_code
        guest_registration = GuestRegistration.objects.create(
            verification_code=verification_code,
            **validated_data
        )
        # Send a verification email (implemented in tasks.py)
        send_verification_email.delay(
            guest_registration.email,
            guest_registration.verification_code,
            guest_registration.event_id
        )
        return guest_registration

