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
from Accounts.views import RegistrationAPI, LoginAPI, SearchHistoryAPI, BookmarkAPI
from Movie.views import MovieSelectionAPI, MovieHistoryAPI, MoviePlotAPI
from Song.views import SongSelectionAPI, MusicRecommendationAPI

# router = DefaultRouter()
# router.register('register', RegistrationAPI, basename='Registration')
urlpatterns = [
    path('admin/', admin.site.urls), # admin panel
    path('registration/', RegistrationAPI.as_view(), name="Registration"), # Registration API
    path('login/', LoginAPI.as_view(), name="Login"), # Login API
    path('movie/', MovieSelectionAPI.as_view(), name="Movie"), # movie-based search
    path('song/', SongSelectionAPI.as_view(), name='SongAPI'), # lyric-based search
    path('moviehistory/', MovieHistoryAPI.as_view(), name="MovieHistory"), # obsolete
    path('history/', SearchHistoryAPI.as_view(), name="SearhHistory"), # Search history url
    path('plot_movie/', MoviePlotAPI.as_view(), name='Plot'), # Description-based search
    path('bookmark/',BookmarkAPI.as_view(), name="Bookmark"), #Bookmark
    path('musicRecommend/', MusicRecommendationAPI.as_view(), name="MusicRecommendation" ) #Recommendation for music
]
