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

    path('activity/<str:activity>/<str:platform>/', views.activity, name='activity'),
    path('activity/<str:activity>/<str:platform>/<str:date>', views.activity, name='activity'),
    path('register/<str:activity>/<str:platform>/', views.register, name='register'),
    path('register/<str:activity>/<str:platform>/<str:date>', views.register, name='register'),

    path('hourmarker/', views.HourMarkerApi.as_view()),
    path('hourmarker/<int:activity>/<int:platform>/<str:date>/', views.HourMarkerApi.as_view()),
    path('roster/<int:activity>/<int:platform>/<str:date>', views.RosterApi.as_view(), name='roster'),

    path('tag/user/', views.UserTagApi.as_view(), name='user-tag'),
] 




