from django.urls import path
from . import views

urlpatterns = [
    # 영화 기본 기능
    path('search/<query>/', views.movie_search),
    path('<int:movie_pk>/', views.movie_detail),
    path('add_movie_info/<int:movie_pk>/', views.add_movie_info),
    path('<int:movie_pk>/like/', views.movie_like),

    # 추천로직
    # 연령성별, 좋아한 영화(장르), 좋아한 바스켓, 친구가 좋아한 영화
    path('recommend/myinfo/', views.movie_recommend_myinfo),
    path('recommend/genre/', views.movie_recommend_genre),
    path('recommend/baskets/', views.movie_recommend_baskets),
    path('recommend/friends/', views.movie_recommend_friends),

    # tmdb api
    path('tmdb/', views.tmdb_movie),
]