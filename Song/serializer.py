from rest_framework.serializers import ModelSerializer
from .models import  BillBoardLyric, TrackLyric, NewTrackLyric


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