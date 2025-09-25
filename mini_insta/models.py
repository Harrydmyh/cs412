# mini-insta/models.py
# model for the mini-insta application
from django.db import models


# Create your models here.
class Profile(models.Model):
    """Encapsulate the data of the profile of an individual user"""

    # define the data attributes of the Profile object
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """return a string representation of this model instance"""
        return f"{self.display_name}"
