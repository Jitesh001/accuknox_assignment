from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FriendRequest, Friendship

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class FriendRequestSerializer(serializers.ModelSerializer):
    from_user_email = serializers.SerializerMethodField()
    to_user_email = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'from_user_email', 'to_user', 'to_user_email', 'timestamp']

    def get_from_user_email(self, obj):
        return obj.from_user.email

    def get_to_user_email(self, obj):
        return obj.to_user.email

