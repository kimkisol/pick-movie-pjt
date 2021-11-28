from django.db import models
from django.conf import settings


class Actor(models.Model):
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name


class Movie(models.Model):
    actors = models.ManyToManyField(Actor, related_name='movies')
    genres = models.ManyToManyField(Genre, related_name='movies')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
    title = models.CharField(max_length=255, null=False)
    overview = models.TextField(null=True)
    poster_path = models.CharField(max_length=255, null=True)
    vote_average = models.FloatField(null=True)
    release_date = models.DateField(null=True)
    adult = models.BooleanField(null=True)
    runtime = models.IntegerField(null=True)

    def __str__(self):
        return self.title