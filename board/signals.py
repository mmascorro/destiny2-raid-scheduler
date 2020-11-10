from django.dispatch import receiver
from authlib.integrations.django_client import token_update
from .models import OAuth2Token

@receiver(token_update)
def on_token_update(sender, token, refresh_token=None, access_token=None, **kwargs):

    if refresh_token:
        local_token = OAuth2Token.objects.get(refresh_token=refresh_token)
    elif access_token:
        local_token = OAuth2Token.objects.get(access_token=access_token)
    else:
        return

    # update old token
    local_token.access_token = token['access_token']
    local_token.refresh_token = token['refresh_token']
    local_token.expires_at = token['expires_at']
    local_token.save()