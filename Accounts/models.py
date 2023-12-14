from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save #signals
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

class User(AbstractUser):
    pass
# Create your models here.

choices = (
    ("movie", "movie"),
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
    search_id = models.IntegerField()
    search_type = models.CharField(max_length=20, choices=choices, default=None)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user_query 
    

