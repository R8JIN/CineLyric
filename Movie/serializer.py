from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import MovieQuotes
class MovieSerializer(ModelSerializer):
    class Meta:
        model = MovieQuotes
        fields = "__all__"


class QuoteSerializer(ModelSerializer):
    class Meta:
        model = MovieQuotes
        fields =['quote']