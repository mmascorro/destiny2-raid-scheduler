from rest_framework import serializers
from .models import HourMarker, Tag


class HourMarkerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = HourMarker
        fields = ['id', 'activity', 'platform', 'user', 'marker_datetime', 'register_on']

class TagSerializer(serializers.ModelSerializer):
    class  Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'description', 'user']