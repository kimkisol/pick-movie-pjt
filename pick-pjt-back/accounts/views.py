from django.db.models.aggregates import Count
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie

# model
from django.contrib.auth import get_user_model
from accounts.models import Group, Relationship
from baskets.models import Basket, BasketTag
from movies.models import Movie

# serializer
from .serializers import GroupListSerialzier, GroupSerialzier, RelationshipListSerializer, RelationshipSerializer, UserListSerializer, UserSerializer
from baskets.serializers import BasketListSerializer
from movies.serializers import MovieListSerializer

# REST framework
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# orm
from django.db.models import Count


# 회원가입 가져오기 (기본그룹 생성)
@api_view(['POST'])
def signup(request):
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')

    if password != password_confirmation:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        user.set_password(request.data.get('password'))
        user.save()
        Group.objects.create(user=user) # 기본 그룹생성
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def login(request):
    return Response({ 'userId': request.user.pk }, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def user_info(request):
    users = get_user_model().objects.all()
    serializer = UserListSerializer(users, many=True)
    return Response(serializer.data)


# profile에서 유저와 관련된 데이터 다 가져와야됨
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        image = request.data.get('image') # 필수인지 확인
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(image=image)
            return Response(serializer.data)

    elif request.method == 'DELETE':
        user_pk = request.user.pk
        request.user.delete()
        return Response({ 'delete': f'{user_pk} 회원이 탈퇴했습니다.' }, status=status.HTTP_204_NO_CONTENT)


# 유저가 쓴 바스켓 리스트, 유저가 좋아요한 바스켓 리스트, 유저가 좋아요한 영화 리스트
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def add_profile_info(request, user_pk, content_type, content):
    if content_type == 'like':
        if content == 'basket':
            baskets = Basket.objects.filter(like_users=user_pk)
            serializer = BasketListSerializer(baskets, many=True)
            return Response(serializer.data)
        elif content == 'movie':
            movies = Movie.objects.filter(like_users=user_pk)
            serializer = MovieListSerializer(movies, many=True)
            return Response(serializer.data)
    elif content_type == 'write':
        if content == 'basket':
            baskets = Basket.objects.filter(author=user_pk)
            serializer = BasketListSerializer(baskets, many=True)
            return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def liked_baskets_tags(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)

    liked_baskets_ids_obj = list(Basket.objects.filter(like_users=user).values('id'))
    liked_baskets_ids = [obj['id'] for obj in liked_baskets_ids_obj]
    liked_baskets_tags_obj = list(BasketTag.objects.filter(baskets__in=liked_baskets_ids).values('name').annotate(tags_count=Count('id')).order_by('-tags_count')[:3])
    liked_baskets_tags = [obj['name'] for obj in liked_baskets_tags_obj]
    return Response({ 'liked_baskets_tags': liked_baskets_tags }, status=status.HTTP_200_OK)


# Group (RC)
@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def group_list_create(request):
    if request.method == 'GET':
        # groups = Group.objects.filter(user=1) # 테스트용
        groups = Group.objects.filter(user=request.user.pk)
        serializer = GroupListSerialzier(groups, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # user = get_object_or_404(get_user_model(), pk=1) 테스트용
        user = get_object_or_404(get_user_model(), pk=request.user.pk)
        serializer = GroupSerialzier(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                user = user,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# Group (D)
@api_view(['DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def group_delete(request, group_pk):
    group = Group.objects.filter(pk=group_pk)
    group.delete()
    data = {
        'delete': '그룹이 삭제되었습니다.'
    }
    return Response(data, status=status.HTTP_204_NO_CONTENT)


# Relationship (R) - 관계 조회
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def relationship_list(request):
    # relationships = Relationship.objects.filter(fan=1) # 테스트용
    relationships = Relationship.objects.filter(fan=request.user.pk)
    serializer = RelationshipListSerializer(relationships, many=True)
    return Response(serializer.data)


# Relationship (U) - 그룹 이동
@api_view(['PUT'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def relationship_update(request, relationship_pk, group_pk):
    relationship = get_object_or_404(Relationship, pk=relationship_pk)
    star = relationship.star
    
    # fan = get_object_or_404(get_user_model(), pk=1) # 테스트용
    fan = get_object_or_404(get_user_model(), pk=request.user.pk)
    # star = get_object_or_404(get_user_model(), pk=star_pk)

    group = get_object_or_404(Group, pk=group_pk)
    serializer = RelationshipSerializer(instance=relationship, data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(
            fan=fan,
            star=star,
            group=group,
        )
        return Response(serializer.data)


# Relationship (C) - 팔로우('기본' 그룹으로 들어가게 처리)
@api_view(['POST', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def relationship_create_delete(request, star_pk):
    # fan = get_object_or_404(get_user_model(), pk=2)  # 테스트용
    fan = request.user
    star = get_object_or_404(get_user_model(), pk=star_pk)
    if request.method == 'POST':
        group = get_object_or_404(Group, user=fan, name='기본') # 기본 그룹
        # print('팔로우')
        if fan != star:
            serializer = RelationshipSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(
                    fan=fan,
                    star=star,
                    group=group,
                )
                print()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        # print('언팔로우')
        relationship = get_object_or_404(Relationship, fan=fan, star=star)
        # relationship = get_object_or_404(Relationship, pk=15)
        relationship.delete()
        data = {
            'delete': '언팔로우 처리되었습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

# Relationship (D) - 팔로우 취소
# @api_view(['DELETE'])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
# def relationship_delete(request, relationship_pk):
#     relationship = get_object_or_404(Relationship, pk=relationship_pk)
#     relationship.delete()
#     data = {
#         'delete': '언팔로우 처리되었습니다.'
#     }
#     return Response(data, status=status.HTTP_204_NO_CONTENT)
