from django.contrib import admin
from .models import User, SearchHistory
# Register your models here.
admin.site.register(User)
admin.site.register(SearchHistory)