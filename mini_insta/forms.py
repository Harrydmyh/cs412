# mini-insta/forms.py
# forms for creating post in the mini-insta application

from django import forms
from .models import *


class CreatePostForm(forms.ModelForm):
    """A form to add a Post to the database"""

    image_url = forms.URLField(label="Your desired photo for the post")

    class Meta:
        """associate this form with a model from our database"""

        model = Post
        fields = ["caption"]
        labels = {"caption": "Your post content"}
