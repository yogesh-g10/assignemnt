from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import PasswordField

from blog.models import AppUser, Event


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = PasswordField(required=True)

    def create(self, validated_data):
        user: AppUser = authenticate(**validated_data)
        if not user or not user.is_active:
            raise AuthenticationFailed('Username or password is incorrect.')
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id', 'username', 'first_name', 'last_name']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
