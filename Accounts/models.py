from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save #signals
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

class User(AbstractUser):
    

    def __str__(self) -> str:
        return self.username
# Create your models here.


#Flag for different search types: 
# For quote based search, it's movie. 
# For plot based search, flag is plot. 
# For lyric based search, flag is music
choices = (
    ("movie", "movie"),
    ("plot", "plot"),
    ("music", "music")
)

#Token when user is registered
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_query = models.CharField(max_length = 255)
    # search_id = models.IntegerField()
    search_type = models.CharField(max_length=20, choices=choices, default=None)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user.username}:' f'{self.search_type}' 


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    bid = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    image_link = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=choices, default=None)
    datetime = models.DateTimeField(auto_now=True)

    
