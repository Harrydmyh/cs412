# blog/serializers.py
# convert our django data models to a text-representation

from rest_framework import serializers
from .models import *


class ArticleSerializer(serializers.ModelSerializer):
    """
    A serializer for the Article model
    Specify which model/fields to send in the API
    """

    class Meta:
        model = Article
        fields = ["id", "title", "author", "text", "published", "image_file"]

    # add methods to customize the CRUD operations
    def create(self, validated_data):
        """
        override the superclass method that handles object creation
        """
        # create an Article object
        article = Article(**validated_data)
        # attach a FK for the User
        article.user = User.objects.first()
        # save the object to the database
        article.save()
        return article
