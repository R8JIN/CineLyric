from rest_framework.serializers import ModelSerializer
from .models import SongLyric
class SongSerializer(ModelSerializer):
    class Meta:
        model = SongLyric
        fields = "__all__"