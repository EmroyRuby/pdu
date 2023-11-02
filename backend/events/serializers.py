from rest_framework import serializers

from .models import Event, EventNotification, RegistrationResponse, EventRegistration, Category, Comment
from accounts.models import AppUser


class EventSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Category.objects.all(),
        required=False
    )
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'location', 'is_public', 'price', 'capacity',
                  'registration_end_date', 'start_date', 'end_date', 'created_at', 'updated_at',
                  'user', 'user_email', 'categories', 'photo')
        read_only_fields = ('user', 'user_email',)  # setting user as read-only

    def get_user_email(self, obj):
        user = AppUser.objects.get(user_id=obj.user_id)
        return user.email


class EventNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventNotification
        fields = '__all__'


class RegistrationResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationResponse
        fields = '__all__'


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ('event', 'event_title', 'user', 'user_email', 'response', 'response_content'
                  , 'registration_date', 'updated_at')

    user_email = serializers.SerializerMethodField()
    response_content = serializers.SerializerMethodField()
    event_title = serializers.SerializerMethodField()

    def get_user_email(self, obj):
        user = AppUser.objects.get(user_id=obj.user_id)
        return user.email

    def get_response_content(self, obj):
        response = RegistrationResponse.objects.get(id=obj.response_id)
        return response.content

    def get_event_title(self, obj):
        event = Event.objects.get(id=obj.event_id)
        return event.title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CategoryNameListSerializer(serializers.Serializer):
    name = serializers.CharField()
