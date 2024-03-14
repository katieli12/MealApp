from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Feature(models.Model):
    name = models.CharField(max_length=100)
    details = models.CharField(max_length=500)

class Food(models.Model):
    favorites = models.ManyToManyField(
        User, related_name='favorite', default=None, blank=True)