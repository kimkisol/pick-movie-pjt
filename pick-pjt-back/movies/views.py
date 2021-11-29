from django.contrib.auth import get_user_model
from django.http.response import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404

# REST framework
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# model, serializer
from baskets.models import Basket
from .models import Movie, Genre, Actor
from .serializers import MovieDetailSerializer, MovieListSerializer
from baskets.serializers import BasketListSerializer

# orm
from django.db.models import Q, Count
import random
from datetime import timedelta

# api
from decouple import config
from rest_framework.decorators import api_view
import requests

# login user
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


# movie search (index, 영화섹션용) - 영화명, 배우, 장르 기준 검색 (평점순 정렬)
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_search(request, query):
    movies = Movie.objects.filter(
        Q(title__icontains=query)|
        Q(actors__name__icontains=query)|
        Q(genres__name__icontains=query)
        ).distinct().order_by('-vote_average')
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


# movie detail
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieDetailSerializer(movie)
    return Response(serializer.data)


# 이 영화가 포함된 바스켓 리스트
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def add_movie_info(request, movie_pk):
    baskets = Basket.objects.filter(movies=movie_pk)
    serializer = BasketListSerializer(baskets, many=True)
    return Response(serializer.data)


# movie 좋아요 기능
@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_like(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    print('userId', request.user.pk)
    # 테스트용
    # user = get_object_or_404(get_user_model(), pk=1)
    # if movie.like_users.filter(pk=user.pk).exists():
    #     movie.like_users.remove(user)
    #     liked = False
    # else:
    #     movie.like_users.add(user)
    #     liked = True

    if movie.like_users.filter(pk=request.user.pk).exists():
        movie.like_users.remove(request.user)
        liked = False
    else:
        movie.like_users.add(request.user)
        liked = True
    data = {
        'movie': movie_pk,
        'liked': liked,
        'cnt_likes': movie.like_users.count(),
    }
    print(data)
    return Response(data, status=status.HTTP_200_OK)


# 추천: 연령, 성별
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_recommend_myinfo(request):

    # 테스트용
    # user = get_object_or_404(get_user_model(), pk=3)
    # start_date = user.birthdate - timedelta(weeks=260)
    # end_date = user.birthdate + timedelta(weeks=260)
    # q = Q()
    # q.add(
    #     Q(like_users__birthdate__range=(start_date, end_date)),
    #     q.AND
    # )
    # q.add(
    #     Q(like_users__gender=user.gender),
    #     q.AND
    # )
    
    start_date = request.user.birthdate - timedelta(weeks=260)
    end_date = request.user.birthdate + timedelta(weeks=260)

    q = Q()
    q.add(
        Q(like_users__birthdate__range=(start_date, end_date)),
        q.AND
    )
    q.add(
        Q(like_users__gender=request.user.gender),
        q.AND
    )
    filtered_movie_ids = list(Movie.objects.filter(q).distinct().values('id'))

    if len(filtered_movie_ids) >= 6:
        picked_movie_ids_obj = random.sample(filtered_movie_ids, 6)

        picked_movie_ids = [obj['id'] for obj in picked_movie_ids_obj] 
        picked_movies = Movie.objects.filter(pk__in=picked_movie_ids).order_by('-vote_average')

        serializer = MovieListSerializer(picked_movies, many=True)
        recommended_name = '당신 또래의 같은 성별'
        
        new_serializer_data = list(serializer.data)
        new_serializer_data.append({ 'recommended_name': recommended_name })
        return Response(new_serializer_data, status=status.HTTP_200_OK)
    else:
        picked_movies = Movie.objects.all().annotate(like_users_count=Count('like_users')).order_by('-like_users_count')[:6]
        serializer = MovieListSerializer(picked_movies, many=True)
        recommended_name = '지금 핫한'
        
        new_serializer_data = list(serializer.data)
        new_serializer_data.append({ 'recommended_name': recommended_name })
        return Response(new_serializer_data, status=status.HTTP_200_OK)




# 추천 : 좋아하는 장르 TOP3 중 1개 랜덤으로 뽑아 영화 추천
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_recommend_genre(request):
    # favorite_genres = list(Movie.objects.filter(like_users__pk=6).values('genres').annotate(genres_count=Count('genres')).order_by('-genres_count'))[:3] # 테스트용
    favorite_genres = list(Movie.objects.filter(like_users__pk=request.user.pk).values('genres').annotate(genres_count=Count('genres')).order_by('-genres_count'))[:3]

    if len(favorite_genres) > 0:
        random_id = random.sample(favorite_genres, 1)
        filtered_movies_ids = list(Movie.objects.filter(genres__pk=random_id[0]['genres']).distinct().values('id')) ### Population must be a sequence.  For dicts or sets, use sorted(d).
        picked_movies_ids_obj = random.sample(filtered_movies_ids, 6)
        recommended_name = get_object_or_404(Genre, pk=random_id[0]['genres']).name
    else: # 좋아하는 장르가 없는 경우
        genres = list(Genre.objects.values('id'))
        random_id = random.sample(genres, 1)
        picked_movies_ids_obj = random.sample(list(Movie.objects.filter(genres__id=random_id[0]['id']).values('id')), 6)
        recommended_name = get_object_or_404(Genre, pk=random_id[0]['id']).name

    picked_movies_ids = [obj['id'] for obj in picked_movies_ids_obj]
    picked_movies = Movie.objects.filter(pk__in=picked_movies_ids).order_by('-vote_average')

    serializer = MovieListSerializer(picked_movies, many=True)
    new_serializer_data = list(serializer.data)
    new_serializer_data.append({ 'recommended_name': recommended_name })

    return Response(new_serializer_data, status=status.HTTP_201_CREATED)

# 추천: 좋아한 바스켓들에 들어있는 영화들 추천하고, 바스켓 중 하나 이름 추출 ("<음악영화> 바스켓 외 유저님이 좋아한 바스켓의 영화 추천")
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_recommend_baskets(request):
    # liked_baskets = list(Basket.objects.filter(like_users__pk=1).values('id')) # 테스트용
    liked_baskets = list(Basket.objects.filter(like_users__pk=request.user.pk).values('id'))

    if len(liked_baskets) > 5:
        random_ids_obj = random.sample(liked_baskets, 6)
        random_ids = [obj['id'] for obj in random_ids_obj]
        filtered_movies_ids = list(Movie.objects.filter(movies_baskets__pk__in=random_ids).distinct().values('id')) ### Population must be a sequence.  For dicts or sets, use sorted(d).
        picked_movies_ids_obj = random.sample(filtered_movies_ids, 6)
    else: # 좋아하는 바스켓이 6개 미만인 경우
        baskets = list(Basket.objects.values('id'))
        random_ids_obj = random.sample(baskets, 6)
        if baskets:
            random_ids = [obj['id'] for obj in random_ids_obj]
            filtered_movies_ids = list(Movie.objects.filter(movies_baskets__pk__in=random_ids).distinct().values('id'))
            picked_movies_ids_obj = random.sample(filtered_movies_ids, 6)
        else:
            picked_movies = Movie.objects.all().annotate(like_users_count=Count('like_users')).order_by('-like_users_count')[:6]
            serializer = MovieListSerializer(picked_movies, many=True)
            recommended_name = '지금 핫한'
            
            new_serializer_data = list(serializer.data)
            new_serializer_data.append({ 'recommended_name': recommended_name })
            return Response(new_serializer_data, status=status.HTTP_200_OK)

    picked_movies_ids = [obj['id'] for obj in picked_movies_ids_obj]
    picked_movies = Movie.objects.filter(pk__in=picked_movies_ids).order_by('-vote_average')

    serializer = MovieListSerializer(picked_movies, many=True)
    recommended_name = get_object_or_404(Basket, pk=random.sample(random_ids, 1)[0]).title
    new_serializer_data = list(serializer.data)
    new_serializer_data.append({ 'recommended_name': recommended_name })
    return Response(new_serializer_data, status=status.HTTP_201_CREATED)

# 추천: star가 좋아한 영화 추천 (6개 이상 )
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_recommend_friends(request):
    # user = get_object_or_404(get_user_model(), pk=3) # 테스트용
    # stars = list(user.stars.values('id').annotate(movies_count=Count('like_movies')).filter(movies_count__gte=6)) # 테스트용
    stars = list(request.user.stars.values('id').annotate(movies_count=Count('like_movies')).filter(movies_count__gte=6)) # movie 개수가 6개이상인 것만 필터링

    if len(stars) > 0:
        random_id = random.sample(stars, 1)
        q = Q()
        q.add(
            Q(like_users__id=random_id[0]['id']),
            q.OR
        )
        filtered_movie_ids = list(Movie.objects.filter(q).distinct().values('id'))
        picked_movie_ids_obj = random.sample(filtered_movie_ids, 6)
    else: # 팔로우하는 유저가 없거나, 팔로우하는 유저들이 전부 영화 좋아하는 개수가 6개 미만인 경우
        stars = list(get_user_model().objects.values('id').annotate(movies_count=Count('like_movies')).filter(movies_count__gte=6))
        if stars:
            random_id = random.sample(stars, 1)
            picked_movie_ids_obj = random.sample(list(Movie.objects.filter(like_users__pk=random_id[0]['id']).values('id')), 6)
        else:
            picked_movies = Movie.objects.all().annotate(like_users_count=Count('like_users')).order_by('-like_users_count')[:6]
            serializer = MovieListSerializer(picked_movies, many=True)
            recommended_name = '지금 핫한'
            
            new_serializer_data = list(serializer.data)
            new_serializer_data.append({ 'recommended_name': recommended_name })
            return Response(new_serializer_data, status=status.HTTP_200_OK)

    picked_movie_ids = [obj['id'] for obj in picked_movie_ids_obj]
    picked_movies = Movie.objects.filter(pk__in=picked_movie_ids).order_by('-vote_average')

    serializer = MovieListSerializer(picked_movies, many=True)
    recommended_name = get_object_or_404(get_user_model(), pk=random_id[0]['id']).nickname
    new_serializer_data = list(serializer.data)
    new_serializer_data.append({ 'recommended_name': recommended_name })

    return Response(new_serializer_data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def tmdb_movie(request):
    TMDB_API_KEY = config("TMDB_API_KEY")
    for page in range(101, 301):
        url = f'https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=ko&page={page}'
        request = requests.get(url).json()
        for result in request.get('results'):
            movie_id = str(result.get('id'))
            # genre, runtime
            detail_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=ko'
            detail_result = requests.get(detail_url).json()
            # actors
            credit_url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}&language=ko'
            credit_result = requests.get(credit_url).json()
            if result.get('release_date') == '':
                movie = Movie.objects.create(
                    title = result.get('title'),
                    overview = result.get('overview'),
                    poster_path = result.get('poster_path'),
                    vote_average = result.get('vote_average'),
                    adult = result.get('adult'),
                    runtime = detail_result.get('runtime'),
                )
            else:
                movie = Movie.objects.create(
                    title = result.get('title'),
                    overview = result.get('overview'),
                    poster_path = result.get('poster_path'),
                    vote_average = result.get('vote_average'),
                    release_date = result.get('release_date'),
                    adult = result.get('adult'),
                    runtime = detail_result.get('runtime'),
                )
            # 장르 처리
            for genre_name in detail_result.get('genres'):
                if Genre.objects.filter(name=genre_name.get('name')).exists():
                    genre = get_object_or_404(Genre, name=genre_name.get('name'))
                else:
                    genre = Genre.objects.create(name=genre_name.get('name'))
                # genre = Genre.objects.get(name=genre_name.get('name')) ### create로 하면 중복데이터 저장됨
                genre.movies.add(movie)
            # 배우 처리
            casts = credit_result.get('cast')
            count_actors = 0
            for i in range(len(casts)):
                if casts[i].get('known_for_department') == 'Acting':
                    if Actor.objects.filter(name=casts[i].get('name')).exists():
                        actor = get_object_or_404(Actor, name=casts[i].get('name'))
                    else:
                        actor = Actor.objects.create(name=casts[i].get('name'))
                    movie.actors.add(actor)
                    count_actors += 1
                    if count_actors == 6:
                        break
    return Response({ 'db': '가져왔습니다.' })