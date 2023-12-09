from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

#Serializer for Registration
class AccountSerializer(ModelSerializer):

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(AccountSerializer, self).create(validated_data)
    class Meta:
        model = User
        fields = ('username', 'password')

#Serializer for Login
class LoginSerializer(ModelSerializer):
    username = serializers.CharField()
    class Meta:
        model = User
        fields = ('username', 'password')