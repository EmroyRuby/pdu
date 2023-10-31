from rest_framework import serializers
from django.contrib.auth import authenticate
from accounts.models import AppUser
from rest_framework.exceptions import ValidationError

UserModel = AppUser


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('email', 'username', 'password')  # Explicitly state the fields
        extra_kwargs = {'password': {'write_only': True}}  # Password should be write-only

    def create(self, clean_data):
        return UserModel.objects.create_user(email=clean_data['email'],
                                             password=clean_data['password'],
                                             username=clean_data['username'])


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)  # Although not returned, good to be explicit

    def check_user(self, clean_data):
        user = authenticate(username=clean_data['email'], password=clean_data['password'])
        if not user:
            raise ValidationError('Invalid login credentials')
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('email', 'username')
