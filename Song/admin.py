from django.contrib import admin
from .models import SongLyric, MusicLyric

# Register your models here.
admin.site.register(MusicLyric)
admin.site.register(SongLyric)