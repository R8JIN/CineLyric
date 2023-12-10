from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save #signals
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

class User(AbstractUser):
    pass
# Create your models here.


#Token when user is registered
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

