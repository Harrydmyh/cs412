# mini-insta/forms.py
# forms for creating post in the mini-insta application
# Author: Yihang Duanmu (harrydm@bu.edu), 10/16/2025

from django import forms
from .models import *


class CreatePostForm(forms.ModelForm):
    """A form to add a Post to the database"""

    class Meta:
        """associate this form with a model from our database"""

        model = Post
        fields = ["caption"]
        labels = {"caption": "Your post content"}


class UpdateProfileForm(forms.ModelForm):
    """A form to handle an update to a Profile"""

    class Meta:
        """associate this form with a model from our database"""

        model = Profile
        fields = ["display_name", "profile_image_url", "bio_text"]
        labels = {
            "display_name": "Display name",
            "profile_image_url": "Profile image url",
            "bio_text": "Bio text",
        }


class UpdatePostForm(forms.ModelForm):
    """A form to handle an update to a Post"""

    class Meta:
        """associate this form with a model from our database"""

        model = Post
        fields = ["caption"]
        labels = {
            "caption": "Caption",
        }


class CreateProfileForm(forms.ModelForm):
    """A form to add a Post to the database"""

    class Meta:
        """associate this form with a model from our database"""

        model = Profile
        fields = ["username", "display_name", "profile_image_url", "bio_text"]
        labels = {
            "username": "Mini-instagram username",
            "display_name": "Display name",
            "profile_image_url": "Profile image url",
            "bio_text": "Bio text",
        }
