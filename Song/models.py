from django.db import models

# Create your models here.
class SongLyric(models.Model):
    artist_name = models.CharField(max_length=255)
    track_name = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    lyrics = models.TextField()
    release_date = models.IntegerField()

    def __str__(self) -> str:
        return self.track_name 