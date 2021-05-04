from django.db import models
from django.contrib.auth.models import User

class Platform(models.Model):
  name = models.CharField(max_length=20)
  slug = models.SlugField()
  logo = models.CharField(max_length=50)

class Game(models.Model):
  name = models.CharField(max_length=50) 
  platform = models.ManyToManyField(Platform)

class GameActivity(models.Model):
  name = models.CharField(max_length=100)
  slug = models.SlugField()
  game = models.ForeignKey(Game, on_delete=models.CASCADE)
  live_datetime = models.DateTimeField()
  end_datetime = models.DateTimeField(null=True)

class HourMarker(models.Model):
  activity = models.ForeignKey(GameActivity, on_delete=models.CASCADE)
  platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  marker_datetime = models.DateTimeField()
  register_on = models.DateTimeField(auto_now=True)

class DiscordUser(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  id = models.PositiveBigIntegerField(primary_key=True)

class Tag(models.Model):
  user = models.ManyToManyField(User, related_name='tags')
  name = models.CharField(max_length=50, unique=True)
  slug = models.SlugField(unique=True)
  description = models.CharField(max_length=100)


class OAuth2Token(models.Model):
  name = models.CharField(max_length=40)
  token_type = models.CharField(max_length=40)
  access_token = models.CharField(max_length=200)
  refresh_token = models.CharField(max_length=200)
  expires_at = models.PositiveIntegerField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def to_token(self):
      return dict(
          access_token=self.access_token,
          token_type=self.token_type,
          refresh_token=self.refresh_token,
          expires_at=self.expires_at,
      )