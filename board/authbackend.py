from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from authlib.integrations.django_client import OAuth
from .models import OAuth2Token, DiscordUser

class DiscordBackend(BaseBackend):
    def authenticate(self, request, discord_user=None, token=None):
        oauth = OAuth()
        oauth.register('discord')

        #check if user in discord guild
        guilds = oauth.discord.get('users/@me/guilds', token=token).json()
        results = [g for g in guilds if g['id'] == settings.DISCORD_GUILD_ID]
        if len(results) == 1:

            #have local user?
            try:
                d_user = DiscordUser.objects.get(id=discord_user['id'])
                user = d_user.user
                user.username = '{}#{}'.format(discord_user['username'], discord_user['discriminator'])
                user.save()
                
                local_token = OAuth2Token.objects.get(user=user)
                local_token.access_token = token['access_token']
                local_token.refresh_token = token['refresh_token']
                local_token.expires_at = token['expires_at']
                local_token.save()

                return user

            #no local user
            except DiscordUser.DoesNotExist:
                #create local user
                user = User.objects.create_user('{}#{}'.format(discord_user['username'], discord_user['discriminator']))
                user.save()

                new_discord_user = DiscordUser()
                new_discord_user.id = discord_user['id']
                new_discord_user.user = user
                new_discord_user.save()

                #save token
                new_token = OAuth2Token()
                new_token.user = user
                new_token.token_type = token['token_type']
                new_token.access_token = token['access_token']
                new_token.refresh_token = token['refresh_token']
                new_token.expires_at = token['expires_at']
                new_token.save()

                return user

            return None
        else:  
            return None

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None