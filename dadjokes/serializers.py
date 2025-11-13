# dadjokes/serializers.py
# serializers for the dadjokes application
# Author: Yihang Duanmu (harrydm@bu.edu), 11/11/2025

from rest_framework import serializers
from .models import *


class JokeSerializer(serializers.ModelSerializer):
    """
    A serializer for the Joke model
    Specify which model/fields to send in the API
    """

    class Meta:
        model = Joke
        fields = ["id", "text", "author", "timestamp"]


class PictureSerializer(serializers.ModelSerializer):
    """
    A serializer for the Picture model
    Specify which model/fields to send in the API
    """

    class Meta:
        model = Picture
        fields = ["id", "image_url", "author", "timestamp"]
