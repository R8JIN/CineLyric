from rest_framework.serializers import ModelSerializer
from .models import  NewTrackLyric, SpotifyMusicLyric




class NewTrackSerializer(ModelSerializer):
    class Meta:
        model = NewTrackLyric
        fields = "__all__"

class SpotifyTrackSerializer(ModelSerializer):
    class Meta:
        model = SpotifyMusicLyric
        fields = "__all__"