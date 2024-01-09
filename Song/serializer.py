from rest_framework.serializers import ModelSerializer
from .models import SongLyric, MusicLyric, BillBoardLyric
class SongSerializer(ModelSerializer):
    class Meta:
        model = SongLyric
        fields = "__all__"

class MusicSerializer(ModelSerializer):
    class Meta:
        model = BillBoardLyric
        fields = ['track_name', 'artist_name']

