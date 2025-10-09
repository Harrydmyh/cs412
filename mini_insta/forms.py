# mini-insta/forms.py
# forms for creating post in the mini-insta application

from django import forms
from .models import *


class CreatePostForm(forms.ModelForm):
    """A form to add a Post to the database"""

    image_files = forms.ImageField(
        required=False,
        label="Upload your desired photo for the post",
    )

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
