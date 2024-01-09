from django.contrib import admin
from .models import SongLyric, MusicLyric, BillBoardLyric

# Register your models here.
admin.site.register(MusicLyric)
admin.site.register(SongLyric)
admin.site.register(BillBoardLyric)