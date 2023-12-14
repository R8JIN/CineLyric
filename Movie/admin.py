from django.contrib import admin
from .models import MovieQuotes, MovieSearchHistory
# Register your models here.
admin.site.register(MovieQuotes)
admin.site.register(MovieSearchHistory)
