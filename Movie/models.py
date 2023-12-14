from django.db import models
from Accounts.models import User
# Create your models here.
class MovieQuotes(models.Model):
    quote = models.CharField(max_length=255)
    movie = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    year = models.CharField(max_length=255)


    def __str__(self) -> str:
        return self.movie

class MovieSearchHistory(models.Model):
    movie = models.ForeignKey(MovieQuotes, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_quote = models.CharField(max_length=255, default=None)
    datetime = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return f'{self.user_quote} {self.user.username}'