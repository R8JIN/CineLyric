from rest_framework.serializers import ModelSerializer
from .models import SongLyric, MusicLyric, BillBoardLyric, TrackLyric
class SongSerializer(ModelSerializer):
    class Meta:
        model = SongLyric
        fields = "__all__"

class MusicSerializer(ModelSerializer):
    class Meta:
        model = BillBoardLyric
        fields = "__all__"

class TrackSerializer(ModelSerializer):
    class Meta:
        model = TrackLyric
        fields = "__all__"
