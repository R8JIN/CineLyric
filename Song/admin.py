from django.contrib import admin
from .models import  BillBoardLyric, TrackLyric, NewTrackLyric

# Register your models here.

admin.site.register(BillBoardLyric)
admin.site.register(TrackLyric)
admin.site.register(NewTrackLyric)