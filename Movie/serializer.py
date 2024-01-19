from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import MovieQuotes, MovieSearchHistory, MovieSynopsis, Quotation, MovieQuoteOverview


class MovieQuoteSerializer(ModelSerializer):
    class Meta:
        model = MovieQuoteOverview
        fields = "__all__"

#obsolete
class MovieSerializer(ModelSerializer):
    class Meta:
        model = MovieQuotes
        fields = "__all__"

#obsolete
class QuoteSerializer(ModelSerializer):
    class Meta:
        model = Quotation
        fields = "__all__"

class PlotSerializer(ModelSerializer):
    class Meta:
        model = MovieSynopsis
        fields = "__all__"

#obsolete
class MovieSearchHistorySerializer(ModelSerializer):
    class Meta:
        model = MovieSearchHistory
        fields = "__all__"