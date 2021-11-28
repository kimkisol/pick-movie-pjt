from datetime import timedelta
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import get_user_model

# REST framework
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# orm
from django.db.models import Q, Count

# model, serializer
from movies.models import Movie
from .models import Basket, Comment, BasketTag
from .serializers import BasketListSerializer, BasketSerializer, CommentSerializer

# 추천 로직
import random


# Basket (C) - 바스켓 생성
@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def basket_create(request):
    ### movies = get_list_or_404(Movie) 첫번째 에러 이거 외래키라 여기서 처리하는 거 아님...
    # author = get_object_or_404(get_user_model(), pk=1) # 테스트용
    author = get_object_or_404(get_user_model(), pk=request.user.pk)

    serializer = BasketSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(
            author = author,
            # movies = movies, ### 위와 같은 오류
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Basket (R) - 바스켓 리스트(유저)
# @api_view(['GET'])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
# def user_basket_list(request, user_pk, type, contents):
#     # baskets = Basket.objects.filter(author=1)
#     baskets = Basket.objects.filter(author=user_pk)
#     serializer = BasketListSerializer(baskets, many=True)
#     return Response(serializer.data)


# # Basket (R) - 바스켓 리스트(영화)
# @api_view(['GET'])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
# def movie_basket_list(request, movie_pk):
#     baskets = Basket.objects.filter(movies__in=movie_pk)
#     serializer = BasketListSerializer(baskets, many=True)
#     return Response(serializer.data)


# Basket (RUD) - 바스켓 디테일 조회, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def basket_detail_update_delete(request, basket_pk):
    basket = get_object_or_404(Basket, pk=basket_pk)

    if request.method == 'GET':
        serializer = BasketSerializer(basket)
        return Response(serializer.data)
        
    elif request.method == 'PUT':
        # movies = get_list_or_404(Movie) ### 위와 같은 오류
        author = get_object_or_404(get_user_model(), pk=request.user.pk)
        author = get_object_or_404(get_user_model(), pk=1)
        
        serializer = BasketSerializer(instance=basket, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                # movies=movies, ### 위와 같은 오류
                author=author,
            )
            return Response(serializer.data)

    elif request.method == 'DELETE':
        basket.delete()
        data = {
            'delete': '바스켓이 삭제되었습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)


# Comment (CR) - 댓글 생성, 조회
@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_list_create(request, basket_pk):

    if request.method == 'GET':
        # comments = get_list_or_404(Comment, basket=basket_pk)
        comments = Comment.objects.filter(basket=basket_pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        basket = get_object_or_404(Basket, pk=basket_pk)
        author = get_object_or_404(get_user_model(), pk=request.user.pk)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                author=author,
                basket=basket,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# Comment (D) - 댓글 삭제
@api_view(['DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_delete(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.user == comment.author:
        comment.delete()
        data = {
            'delete' : f'{comment_pk}번 댓글이 삭제되었습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)


# 추천 : 성별, 연령이 유사한 유저가 좋아한 바스켓  (태그명 똑같이 통일 "유사한 성연령대의 p!cker들이 좋아한 바스켓")
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def basket_recommend_myinfo(request):
    # 테스트용 코드
    # user = get_object_or_404(get_user_model(), pk=4)
    # start_date = user.birthdate - timedelta(weeks=260)
    # end_date = user.birthdate + timedelta(weeks=260) ### years 안됨
    # q = Q()
    # q.add(
    #     Q(like_users__birthdate__range=(start_date, end_date)),
    #     q.AND
    # )
    # q.add(
    #     Q(like_users__gender=user.gender),
    #     q.AND
    # )
    # q.add( # public이거나 participants에 user가 포함된 경우만
    #     Q(public=True)|
    #     Q(participants__pk=user.pk),
    #     q.AND
    # )
    # filtered_basket_ids = list(Basket.objects.filter(q).distinct().values('id')) ### 리스트 필수
    start_date = request.user.birthdate - timedelta(weeks=260)  
    end_date = request.user.birthdate + timedelta(weeks=260) ### years 안됨

    q = Q()
    q.add(
        Q(like_users__birthdate__range=(start_date, end_date)),
        q.AND
    )
    q.add(
        Q(like_users__gender=request.user.gender),
        q.AND
    )
    q.add( # public이거나 participants에 user가 포함된 경우만
        Q(public=True)|
        Q(participants__pk=request.user.pk),
        q.AND
    )
    filtered_basket_ids = list(Basket.objects.filter(q).distinct().values('id'))

    if len(filtered_basket_ids) >= 3:
        picked_basket_ids_obj = random.sample(filtered_basket_ids, 3)
        picked_basket_ids = [obj['id'] for obj in picked_basket_ids_obj] ### obj형식으로 도는거라 따로 추출해줘야 함
        picked_baskets = Basket.objects.filter(pk__in=picked_basket_ids).annotate(like_users_count=Count('like_users')).order_by('-like_users_count')

        serializer = BasketListSerializer(picked_baskets, many=True)
        recommended_name = '당신 또래의 같은 성별'
        
        new_serializer_data = list(serializer.data)
        new_serializer_data.append({ 'recommended_name': recommended_name })
        return Response(new_serializer_data, status=status.HTTP_200_OK)
    else: # 3개 이하일때는 그냥 전체 랜덤으로
        picked_baskets = Basket.objects.all().annotate(like_users_count=Count('like_users')).order_by('-like_users_count')[:3]
        serializer = BasketListSerializer(picked_baskets, many=True)
        recommended_name = '지금 핫한'
        
        new_serializer_data = list(serializer.data)
        new_serializer_data.append({ 'recommended_name': recommended_name })
        return Response(new_serializer_data, status=status.HTTP_200_OK)


# 추천 : 선호 영화가 들어있는 바스켓
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def basket_recommend_movies(request):
    # user = get_object_or_404(get_user_model(), pk=2) # 테스트용
    # like_movies = list(user.like_movies.values('id').annotate(baskets_count=Count('movies_baskets')).filter(baskets_count__gte=3)) # 테스트용

    like_movies = list(request.user.like_movies.values('id').annotate(baskets_count=Count('movies_baskets')).filter(baskets_count__gte=3)) # basket 개수가 3개이상인 것만 필터링

    if len(like_movies) > 0:
        random_id = random.sample(like_movies, 1)
        q = Q()
        q.add(
            Q(movies__id=random_id[0]['id']),
            q.OR
        )
        q.add(
            Q(public=True)|
            Q(participants__pk=request.user.pk),
            q.AND
        )
        filtered_basket_ids = list(Basket.objects.filter(q).distinct().values('id'))
        picked_basket_ids_obj = random.sample(filtered_basket_ids, 3)
    else: # 좋아한 태그가 없는 경우, 랜덤으로 태그 뽑아서 보여줌
        like_movies = list(Movie.objects.values('id').annotate(baskets_count=Count('movies_baskets')).filter(baskets_count__gte=3))
        if like_movies:
            random_id = random.sample(like_movies, 1)
            picked_basket_ids_obj = random.sample(list(Basket.objects.filter(movies__pk=random_id[0]['id']).annotate(like_users_count=Count('like_users')).values('id')), 3)
        else:
            picked_baskets = Basket.objects.all().annotate(like_users_count=Count('like_users')).order_by('-like_users_count')[:3]
            serializer = BasketListSerializer(picked_baskets, many=True)
            recommended_name = '지금 핫한'
            
            new_serializer_data = list(serializer.data)
            new_serializer_data.append({ 'recommended_name': recommended_name })
            return Response(new_serializer_data, status=status.HTTP_200_OK)

    picked_basket_ids = [obj['id'] for obj in picked_basket_ids_obj]
    picked_baskets = Basket.objects.filter(pk__in=picked_basket_ids).annotate(like_users_count=Count('like_users')).order_by('-like_users_count')

    serializer = BasketListSerializer(picked_baskets, many=True)
    recommended_name = get_object_or_404(Movie, pk=random_id[0]['id']).title
    
    new_serializer_data = list(serializer.data)
    new_serializer_data.append({ 'recommended_name': recommended_name })
    return Response(new_serializer_data, status=status.HTTP_200_OK)

# 추천 : 좋아하는 태그가 들어있는 바스켓
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def basket_recommend_tags(request):
    # user = get_object_or_404(get_user_model(), pk=2) # 테스트용
    # users_baskets_tags = list(user.users_baskets_tags.values('id').annotate(baskets_count=Count('baskets')).filter(baskets_count__gte=3)) # 테스트용
    users_baskets_tags = list(request.user.users_baskets_tags.values('id').annotate(baskets_count=Count('baskets')).filter(baskets_count__gte=3)) # basket 개수가 3개이상인 것만 필터링

    if len(users_baskets_tags) > 0:
        random_id = random.sample(users_baskets_tags, 1)
        q = Q()
        q.add(
            Q(baskets_tags__pk=random_id[0]['id']),
            q.OR
        )
        q.add(
            Q(public=True)|
            Q(participants__pk=request.user.pk),
            q.AND
        )
        filtered_basket_ids = list(Basket.objects.filter(q).distinct().values('id'))
        picked_basket_ids_obj = random.sample(filtered_basket_ids, 3)
    else: # 좋아한 태그가 없는 경우, 랜덤으로 태그 뽑아서 보여줌
        baskets_tags = list(BasketTag.objects.values('id').annotate(baskets_count=Count('baskets')).filter(baskets_count__gte=3))
        if baskets_tags:
            random_id = random.sample(baskets_tags, 1)
            picked_basket_ids_obj = random.sample(list(Basket.objects.filter(baskets_tags__pk=random_id[0]['id']).values('id')), 3)
        else:
            picked_baskets = Basket.objects.all().annotate(like_users_count=Count('like_users')).order_by('-like_users_count')[:3]
            serializer = BasketListSerializer(picked_baskets, many=True)
            recommended_name = '지금 핫한'
            
            new_serializer_data = list(serializer.data)
            new_serializer_data.append({ 'recommended_name': recommended_name })
            return Response(new_serializer_data, status=status.HTTP_200_OK)

    picked_basket_ids = [obj['id'] for obj in picked_basket_ids_obj]
    picked_baskets = Basket.objects.filter(pk__in=picked_basket_ids).annotate(like_users_count=Count('like_users')).order_by('-like_users_count')

    serializer = BasketListSerializer(picked_baskets, many=True)
    recommended_name = get_object_or_404(BasketTag, pk=random_id[0]['id']).name
    new_serializer_data = list(serializer.data)
    new_serializer_data.append({ 'recommended_name': recommended_name })
    return Response(new_serializer_data, status=status.HTTP_200_OK)


# 추천 : 팔로우하는 유저가 좋아한 바스켓
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def basket_recommend_friends(request):
    # user = get_object_or_404(get_user_model(), pk=7) # 테스트용
    # stars = list(user.stars.values('id').annotate(baskets_count=Count('like_baskets')).filter(baskets_count__gte=3)) # 테스트용
    stars = list(request.user.stars.values('id').annotate(baskets_count=Count('like_baskets')).filter(baskets_count__gte=3)) # basket 개수가 3개이상인 것만 필터링

    if len(stars) > 0:
        random_id = random.sample(stars, 1)
        q = Q()
        q.add(
            Q(like_users__id=random_id[0]['id']),
            q.OR
        )
        q.add(
            Q(public=True)|
            Q(participants__pk=request.user.pk),
            q.AND
        )
        filtered_basket_ids = list(Basket.objects.filter(q).distinct().values('id'))
        picked_basket_ids_obj = random.sample(filtered_basket_ids, 3)
    else: # 좋아한 태그가 없는 경우, 랜덤으로 태그 뽑아서 보여줌
        stars = list(get_user_model().objects.values('id').annotate(baskets_count=Count('like_baskets')).filter(baskets_count__gte=3))
        if stars:
            random_id = random.sample(stars, 1)
            picked_basket_ids_obj = random.sample(list(Basket.objects.filter(like_users__pk=random_id[0]['id']).values('id')), 3)
        else:
            picked_baskets = Basket.objects.all().annotate(like_users_count=Count('like_users')).order_by('-like_users_count')[:3]
            serializer = BasketListSerializer(picked_baskets, many=True)
            recommended_name = '지금 핫한'
            
            new_serializer_data = list(serializer.data)
            new_serializer_data.append({ 'recommended_name': recommended_name })
            return Response(new_serializer_data, status=status.HTTP_200_OK)

    picked_basket_ids = [obj['id'] for obj in picked_basket_ids_obj]
    picked_baskets = Basket.objects.filter(pk__in=picked_basket_ids).annotate(like_users_count=Count('like_users')).order_by('-like_users_count')

    serializer = BasketListSerializer(picked_baskets, many=True)
    recommended_name = get_object_or_404(get_user_model(), pk=random_id[0]['id']).nickname
    new_serializer_data = list(serializer.data)
    new_serializer_data.append({ 'recommended_name': recommended_name })

    return Response(new_serializer_data, status=status.HTTP_200_OK)


# basket search (index, 바스켓섹션용) - 바스켓 제목, 바스켓 태그, 작성자, 영화명, 배우에 검색어 검색 (좋아요순으로 정렬)
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def basket_search(request, query):
    q = Q()
    q.add(
        Q(title__icontains=query)|
        Q(baskets_tags__name__icontains=query)|
        Q(author__nickname__icontains=query)|
        Q(movies__title__icontains=query)|
        Q(movies__actors__name__icontains=query)|
        Q(movies__genres__name__icontains=query),
        q.OR
    )
    q.add(
        Q(public=True)|
        Q(participants__nickname__icontains=request.user.nickname),
        q.AND
    )
    baskets = Basket.objects.filter(q).distinct().annotate(like_users_count=Count('like_users')).order_by('-like_users_count')
    serializer = BasketListSerializer(baskets, many=True)

    return Response(serializer.data)


# 좋아요 기능
@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def basket_like(request, basket_pk):
    print('userId', request.user.pk)
    # user = get_object_or_404(get_user_model(), pk=1)
    basket = get_object_or_404(Basket, pk=basket_pk)
    user = get_object_or_404(get_user_model(), pk=request.user.pk)
    print(basket.baskets_tags.all())

    # user = get_object_or_404(get_user_model(), pk=1) ### 와....이것때문이었다.....
    if basket.like_users.filter(pk=user.pk).exists(): ### 태그 뱃지에 대한 고민(어떻게 카운트할 지)
        basket.like_users.remove(user)
        liked = False
    else:
        basket.like_users.add(user)
        liked = True

    print(list(basket.like_users.all()))
    data = {
        'basket': basket_pk,
        'liked': liked,
        'cnt_likes': basket.like_users.count(),
    }
    return Response(data, status=status.HTTP_200_OK) # status도 잘넣어야됨