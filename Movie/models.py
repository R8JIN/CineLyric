from django.db import models

# Create your models here.
class MovieQuotes(models.Model):
    quote = models.CharField(max_length=255)
    movie = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    year = models.CharField(max_length=255)


    def __str__(self) -> str:
        return self.movie