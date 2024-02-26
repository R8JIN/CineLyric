from django.contrib import admin
from .models import User, SearchHistory, Bookmark
# Register your models here.
admin.site.register(User)
admin.site.register(SearchHistory)
admin.site.register(Bookmark)