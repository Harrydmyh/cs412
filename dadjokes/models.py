# dadjokes/models.py
# models for the dadjokes application
# Author: Yihang Duanmu (harrydm@bu.edu), 11/11/2025
from django.db import models


# Create your models here.
class Joke(models.Model):
    """Encapsulate the data of a joke created by a user"""

    # define the data attributes of the Joke object
    text = models.TextField(blank=False)
    author = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """return a string representation of this model instance"""
        return f"Joke by {self.author} on {self.timestamp}"


class Picture(models.Model):
    """Encapsulate the data of a funny picture created by a user"""

    # define the data attributes of the Picture object
    image_url = models.URLField(blank=False)
    author = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """return a string representation of this model instance"""
        return f"Picture by {self.author} on {self.timestamp}"
