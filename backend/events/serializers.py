from rest_framework import serializers

from .models import Event, EventNotification, RegistrationResponse, EventRegistration, Category, EventCategory, Comment
from accounts.models import AppUser

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'title', 'description', 'location', 'is_public', 'price', 'capacity',
                  'registration_end_date', 'start_date', 'end_date', 'created_at', 'updated_at',
                  'user', 'user_email', 'categories')


    def get_categories(self, obj):
        categories = Category.objects.filter(eventcategory__event=obj)
        category_names = [category.name for category in categories]
        return category_names

    def get_user_email(self, obj):
        user = AppUser.objects.get(user_id=obj.user_id)
        return user.email


    categories = serializers.SerializerMethodField()
    user_email = serializers.SerializerMethodField()


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
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class EventCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = EventCategory
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CategoryNameListSerializer(serializers.Serializer):
    name = serializers.CharField()
