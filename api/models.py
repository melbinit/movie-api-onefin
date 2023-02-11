from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Movie(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    genres = models.CharField(max_length=500)

    def __str__(self):
        return self.title
    
class Collection(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    movies = models.ManyToManyField(Movie)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.uuid) + " " + self.title

class RequestsData(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    url = models.CharField(max_length=500)