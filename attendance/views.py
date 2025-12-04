# attendance/views.py
# views for the attendance application
# Author: Yihang Duanmu (harrydm@bu.edu), 12/2/2025

from typing import Any
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
)
from .models import *
import random
from rest_framework import generics


# Create your views here.
class ProfileView(DetailView):
    """A view to show home page for students and instructor"""

    model = Profile
    template_name = "attendance/home.html"
    context_object_name = "profile"


class SigninView(DetailView):
    """A view to show signin page for students"""

    model = Class
    template_name = "attendance/signin.html"
    context_object_name = "class"
