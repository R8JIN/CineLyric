from django.db import models

# obsolete model
class SongLyric(models.Model):
    artist_name = models.CharField(max_length=255)
    track_name = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    lyrics = models.TextField()
    release_date = models.IntegerField()

    def __str__(self) -> str:
        return self.track_name 
    
#obsolete model
class MusicLyric(models.Model):
    artist_name = models.CharField(max_length=255)
    track_name = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    lyrics = models.TextField()
    release_date = models.IntegerField()

    def __str__(self) -> str:
        return self.track_name 

# obsolete model
class BillBoardLyric(models.Model):
    artist_name = models.CharField(max_length=255)
    track_name = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    lyrics = models.TextField()
    release_date = models.FloatField()

    def __str__(self) -> str:
        return self.track_name 
    
class TrackLyric(models.Model):
    artist_name = models.CharField(max_length=255)
    track_name = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    lyrics = models.TextField()
    release_date = models.IntegerField()
    youtube_link = models.URLField(blank=True, null=True)
    spotify_link = models.URLField(blank=True, null=True)
    album = models.CharField(max_length=255, blank=True, null=True)
    
