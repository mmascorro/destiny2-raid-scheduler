from django.urls import path, include
from . import views

# from rest_framework import routers

# router = routers.SimpleRouter()
# router.register(r'demo', UserViewSet)


urlpatterns = [
    path('', views.index, name='homepage'),
    path('login/', views.discord_login, name='login'),
    path('logout/', views.scheduler_logout, name='logout'),
    path('authorize/', views.authorize, name='authorize'),

    path('activity/<str:activity>/', views.activity, name='activity'),
    path('activity/<str:activity>/<str:date>', views.activity, name='activity'),
    path('register/<str:activity>/', views.register, name='register'),
    path('register/<str:activity>/<str:date>', views.register, name='register'),

    path('sheet/<str:activity>/', views.sheet, name='sheet'),


    path('hourmarker/', views.HourMarkerApi.as_view()),
    path('hourmarker/<int:activity>/<str:date>/', views.HourMarkerApi.as_view()),
    path('roster/<int:activity>/<str:date>', views.RosterApi.as_view(), name='roster'),

    path('tag/user/', views.UserTagApi.as_view(), name='user-tag'),
] 




