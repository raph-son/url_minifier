from rest_framework import serializers
from url_shorter.models import Url 


class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ("id", "url", "hash")
