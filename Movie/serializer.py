from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import MovieQuotes, MovieSearchHistory
class MovieSerializer(ModelSerializer):
    class Meta:
        model = MovieQuotes
        fields = "__all__"


class QuoteSerializer(ModelSerializer):
    class Meta:
        model = MovieQuotes
        fields =['quote']

class MovieSearchHistorySerializer(ModelSerializer):
    class Meta:
        model = MovieSearchHistory
        fields = "__all__"