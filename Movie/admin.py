from django.contrib import admin
from .models import MovieQuotes, MovieSearchHistory, MovieSynopsis, Quotation, MovieQuoteOverview, DialogueMovie
# Register your models here.
admin.site.register(MovieQuotes)
admin.site.register(MovieSearchHistory)
admin.site.register(MovieSynopsis)
admin.site.register(Quotation)
admin.site.register(MovieQuoteOverview)
admin.site.register(DialogueMovie)