from rest_framework.serializers import ModelSerializer
from .models import SongLyric, MusicLyric
class SongSerializer(ModelSerializer):
    class Meta:
        model = SongLyric
        fields = "__all__"

class MusicSerializer(ModelSerializer):
    class Meta:
        model = MusicLyric
        fields = "__all__"