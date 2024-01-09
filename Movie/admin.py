from django.contrib import admin
from .models import MovieQuotes, MovieSearchHistory, MovieSynopsis, Quotation
# Register your models here.
admin.site.register(MovieQuotes)
admin.site.register(MovieSearchHistory)
admin.site.register(MovieSynopsis)
admin.site.register(Quotation)
