"""CineLyric URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Accounts.views import RegistrationAPI, LoginAPI
from Movie.views import MovieSelectionAPI, MovieHistoryAPI
from Song.views import SongSelectionAPI

# router = DefaultRouter()
# router.register('register', RegistrationAPI, basename='Registration')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', RegistrationAPI.as_view(), name="Registration"),
    path('login/', LoginAPI.as_view(), name="Login"),
    path('movie/', MovieSelectionAPI.as_view(), name="Movie"),
    path('song/', SongSelectionAPI.as_view(), name='SongAPI'),
    path('moviehistory/', MovieHistoryAPI.as_view(), name="MovieHistory")
]
