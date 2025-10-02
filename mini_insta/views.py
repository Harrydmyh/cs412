# File: mini_insta/views.py
# Author: Yihang Duanmu (harrydm@bu.edu), 9/25/2025
# Description: Views for the mini_insta application

from django.db.models.base import Model as Model
from django.views.generic import ListView, DetailView
from .models import *


# Create your views here.
class ProfileListView(ListView):
    """Define a view class to show all profiles"""

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"


class ProfileDetailView(DetailView):
    """Define a view class to show one profile"""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"


class PostDetailView(DetailView):
    """Define a view class to show one post"""

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"
