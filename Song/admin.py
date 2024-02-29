from django.contrib import admin
from .models import  BillBoardLyric, TrackLyric, NewTrackLyric, SpotifyMusicLyric

# Register your models here.

admin.site.register(BillBoardLyric)
admin.site.register(TrackLyric)
admin.site.register(NewTrackLyric)
admin.site.register(SpotifyMusicLyric)