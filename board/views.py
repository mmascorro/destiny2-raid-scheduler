from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.conf import settings

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import OAuth2Token, DiscordUser, Platform, GameActivity, HourMarker, Tag
from authlib.integrations.django_client import OAuth

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from datetime import datetime, time, timezone
import pytz

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .serializers import HourMarkerSerializer, TagSerializer

def index(request):

  if request.user.is_authenticated:

    activities = GameActivity.objects.all()
    platforms = Platform.objects.all()

    context = {
      'title': settings.PUBLIC_TITLE,
      'activities': activities,
      'platforms': platforms
    }
    return render(request, 'board/auth_index.html', context)

  else:
    context = {
      'title': settings.PUBLIC_TITLE
    }
    return render(request, 'board/public_index.html', context)



def discord_login(request):
    oauth = OAuth()
    oauth.register(
      name='discord',
      client_kwargs={
        'scope': 'identify guilds'
      }
    )
 
    redirect_to = request.build_absolute_uri('/authorize')

    return oauth.discord.authorize_redirect(request, redirect_to)

def scheduler_logout(request):
  logout(request)
  context = {
    'title': 'Logged Out'
  }
  return render(request, 'board/logout.html', context)

def authorize(request):
    oauth = OAuth()
    oauth.register(
      name='discord'
    )

    token = oauth.discord.authorize_access_token(request)
    discord_user_resp = oauth.discord.get('users/@me', token=token).json()

    user = authenticate(discord_user=discord_user_resp, token=token)
    if user:
      login(request, user)
      return redirect('homepage')
    else:
      return HttpResponse('not authorized')

    return HttpResponse('-')


@login_required
def activity(request, activity, platform, date=None):

    platform = Platform.objects.get(slug=platform)
    activity = GameActivity.objects.get(slug=activity, game__platform=platform)

    if not date:
      if datetime.now(timezone.utc) < activity.live_datetime:
        dt = activity.live_datetime.strftime('%Y-%m-%d')
      else:
        dt = datetime.now(timezone.utc).strftime('%Y-%m-%d')
      return redirect(reverse('activity', args=[activity.slug, platform.slug, dt]))

    specified_date = datetime.strptime(date, '%Y-%m-%d')
    if specified_date.date() < activity.live_datetime.date():
      dt = activity.live_datetime.strftime('%Y-%m-%d')
      return redirect(reverse('activity', args=[activity.slug, platform.slug, dt]))


    markers = activity.hourmarker_set.all()
    all_platforms = Platform.objects.all()
    all_tags = Tag.objects.all()
  
    context =  {
      'title': specified_date.strftime('%Y-%m-%d'),
      'specified_date': specified_date,
      'specified_platform': platform,
      'specified_activity': activity,
      'all_platforms': all_platforms,
      'all_tags': all_tags
    }

    return render(request, 'board/activity.html', context)


@login_required
def register(request, activity, platform, date=None):

    platform = Platform.objects.get(slug=platform)
    activity = GameActivity.objects.get(slug=activity, game__platform=platform)

    if not date:
      if datetime.now(timezone.utc) < activity.live_datetime:
        dt = activity.live_datetime.strftime('%Y-%m-%d')
      else:
        dt = datetime.now(timezone.utc).strftime('%Y-%m-%d')
      return redirect(reverse('register', args=[activity.slug, platform.slug, dt]))

    specified_date = datetime.strptime(date, '%Y-%m-%d')

    specified_date = datetime.strptime(date, '%Y-%m-%d')
    if specified_date.date() < activity.live_datetime.date():
      dt = activity.live_datetime.strftime('%Y-%m-%d')
      return redirect(reverse('register', args=[activity.slug, platform.slug, dt]))

    all_platforms = Platform.objects.all()
    all_tags = Tag.objects.all()

    context = {
      'title': specified_date.strftime('%Y-%m-%d'),
      'specified_date': specified_date,
      'specified_platform': platform,
      'specified_activity': activity,
      'all_platforms': all_platforms,
      'all_tags': all_tags

    }
    return render(request, 'board/register.html', context)


class HourMarkerApi(APIView):
    authentication_classes = [SessionAuthentication]

    def get(self, request, activity, platform, date,  format=None):
      specified_date = datetime.strptime(date, '%Y-%m-%d')
      startDateTime = request.GET.get('start')
      endDateTime = request.GET.get('end')

      hm = HourMarker.objects.filter(user=request.user, activity=activity, platform=platform, marker_datetime__range=(startDateTime, endDateTime))
      serializer = HourMarkerSerializer(hm, many=True)
      return Response(serializer.data)
    
    def post(self, request):
      serializer = HourMarkerSerializer(data=request.data, context={'request': request})
      if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)

      else:
        print('not valid')
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
      hm = HourMarker.objects.get(pk=request.data['id'], user=request.user)

      hm.delete()

      return Response({'msg': 'deleted'})




class RosterApi(APIView):

    authentication_classes = [SessionAuthentication]


    def get(self, request, activity, platform, date, format=None):
      specified_date = datetime.strptime(date, '%Y-%m-%d')
      startDateTime = request.GET.get('start')
      endDateTime = request.GET.get('end')


      dsc = GameActivity.objects.get(pk=activity)

      markers = dsc.hourmarker_set.filter(platform=platform, marker_datetime__range=(startDateTime, endDateTime)).order_by('register_on')

      hour_roster = {}
      for hm in markers:
        current_hour = hm.marker_datetime.strftime('%Y-%m-%dT%H:%M')
        if current_hour not in hour_roster:

          hour_roster[current_hour] = []

        player_detail = {
          'user': {
            'id': hm.user.id,
            'name': hm.user.username,
            'tags': []
          },
          'register_on': hm.register_on
        }

        for tag in hm.user.tags.order_by('id'):
          player_detail['user']['tags'].append({
            'id': tag.id,
            'name': tag.name,
            'slug': tag.slug,
            'description': tag.description
          })

        hour_roster[current_hour].append(player_detail)


      return Response(hour_roster)


class UserTagApi(APIView):
    authentication_classes = [SessionAuthentication]

    def get(self, request):
      user = User.objects.get(pk=request.user.id)
      serializer = TagSerializer(user.tags.all(), many=True)

      return Response(serializer.data)

    def post(self, request):
      tag = Tag.objects.get(pk=request.data['id'])
      user = User.objects.get(pk=request.user.id)
      user.tags.add(tag)

      return Response({'msg': 'ok'})

    def delete(self, request):
      tag = Tag.objects.get(pk=request.data['id'])
      user = User.objects.get(pk=request.user.id)
      user.tags.remove(tag)

      return Response({'msg': 'ok'})
