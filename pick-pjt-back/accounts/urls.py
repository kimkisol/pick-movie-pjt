from django.urls import path
from . import views

from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    # 로그인/회원가입
    path('signup/', views.signup),
    path('api-token-auth/', obtain_jwt_token),
    path('login/', views.login),
    path('user_info/', views.user_info),
    path('profile/<int:user_pk>/', views.profile),
    path('add_profile_info/<int:user_pk>/<content_type>/<content>/', views.add_profile_info),
    path('liked_baskets_tags/<int:user_pk>/', views.liked_baskets_tags),

    # 그룹 관리
    path('group/', views.group_list_create),
    path('group/<int:group_pk>/', views.group_delete),
    path('relationship/', views.relationship_list),
    path('relationship/<relationship_pk>/group/<int:group_pk>/', views.relationship_update),
    # path('relationship/<relationship_pk>/star/<int:star_pk>/group/<int:group_pk>/', views.relationship_update),
    # 팔로우
    path('relationship/star/<int:star_pk>/', views.relationship_create_delete),
    # path('relationship/<int:star_/', views.relationship_delete),
]