from django.db import models
from django.conf import settings
from movies.models import Movie


class Basket(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_baskets')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='like_baskets')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='participating_baskets')
    movies = models.ManyToManyField(Movie, related_name='movies_baskets')
    title = models.CharField(max_length=255, null=False)
    explanation = models.TextField()
    public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.TextField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='basket_comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_comments')
    content = models.TextField(null=False)
    spoiler = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class BasketTag(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='users_baskets_tags')
    baskets = models.ManyToManyField(Basket, related_name='baskets_tags')
    name = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.name