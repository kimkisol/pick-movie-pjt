from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Actor, Genre, Movie
from baskets.models import Basket


# MovieSerializer
    # poster_path, title, runtime, vote_average, release_date, actors, genres, overview
    # 바스켓: (역참조) img, title
class MovieDetailSerializer(serializers.ModelSerializer):

    class ActorListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Actor
            fields = '__all__'

    class GenreListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = '__all__'

    class BasketListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Basket
            fields = '__all__'

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('id',) 

    actors = ActorListSerializer(many=True, read_only=True)
    genres = GenreListSerializer(many=True, read_only=True)
    movies_baskets = BasketListSerializer(many=True, read_only=True)
    like_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = (
            'id', 'poster_path', 'title', 'runtime', 'vote_average', 'release_date', 'actors', 'genres', 'overview', 'movies_baskets', 'like_users',
            )
        read_only_fields = ('actors', 'genres', 'movies_baskets',)
    


# poster_path, title, release_date, vote_average
class MovieListSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('id', 'nickname',)

    like_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'release_date', 'poster_path', 'like_users', 'vote_average',)
        read_only_fields = ('like_users',)