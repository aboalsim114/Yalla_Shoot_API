from .models import Message
from rest_framework import serializers
from api.models import User, PlayerProfile, Team, Match, MatchRegistration, SportActivity, Message, Notification
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PlayerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerProfile
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'


class MatchRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchRegistration
        fields = '__all__'


class SportActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SportActivity
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class MessageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=False)
    user_type = serializers.CharField()
    location = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name',
                  'last_name', 'user_type', 'location', 'image']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
