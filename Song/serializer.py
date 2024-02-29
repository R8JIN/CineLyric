from rest_framework.serializers import ModelSerializer
from .models import  BillBoardLyric, TrackLyric, NewTrackLyric, SpotifyMusicLyric


class MusicSerializer(ModelSerializer):
    class Meta:
        model = BillBoardLyric
        fields = "__all__"

class TrackSerializer(ModelSerializer):
    class Meta:
        model = TrackLyric
        fields = "__all__"

class NewTrackSerializer(ModelSerializer):
    class Meta:
        model = NewTrackLyric
        fields = "__all__"

class SpotifyTrackSerializer(ModelSerializer):
    class Meta:
        model = SpotifyMusicLyric
        fields = "__all__"