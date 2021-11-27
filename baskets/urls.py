from django.urls import path
from . import views

urlpatterns = [
    path('', views.basket_create),
    # path('user/<int:user_pk>/', views.user_basket_list),
    # path('movie/<int:movie_pk>/', views.movie_basket_list),
    path('<int:basket_pk>/', views.basket_detail_update_delete),
    path('<int:basket_pk>/comment/', views.comment_list_create),
    path('comment/<int:comment_pk>/', views.comment_delete),

    # 추천로직: 연령성별, 선호영화, 태그, 팔로한사람이좋아한
    path('recommend/myinfo/', views.basket_recommend_myinfo),
    path('recommend/movies/', views.basket_recommend_movies),
    path('recommend/tags/', views.basket_recommend_tags),
    path('recommend/friends/', views.basket_recommend_friends),

    # 검색
    path('search/<query>/', views.basket_search),

    # 좋아요
    path('<int:basket_pk>/like/', views.basket_like),
]
