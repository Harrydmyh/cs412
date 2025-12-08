# attendance/views.py
# views for the attendance application
# Author: Yihang Duanmu (harrydm@bu.edu), 12/2/2025

from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .forms import *
import random
from datetime import datetime, time
import pytz
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


class CreateClassView(CreateView):
    """A view to handle creation of a new Class"""

    model = Profile
    form_class = CreateClassForm
    context_object_name = "profile"
    template_name = "attendance/create_class_form.html"

    def get_success_url(self):
        """Provide a URL to redirect to after creating a new Class"""

        # create and return a URL
        return reverse("home", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        """This method handles the form submission and saves the new object to the Django database"""

        # Create a new user form from POST data
        if self.request.POST:
            print(self.request.POST)
            request = self.request.POST
            class_chosen = request.get("class_name")
            match class_chosen:
                case "CS 412 A1":
                    latitude = 42.350
                    longitude = -71.103
                    date_obj = datetime.strptime(
                        request.get("session_time"), "%Y-%m-%d"
                    ).date()
                    session_time = datetime.combine(date_obj, time(14, 30))
                case "CS 412 B1":
                    latitude = 42.350
                    longitude = -71.103
                    date_obj = datetime.strptime(
                        request.get("session_time"), "%Y-%m-%d"
                    ).date()
                    session_time = datetime.combine(date_obj, time(16, 0))
                case "CS 412 C1":
                    latitude = 42.349
                    longitude = -71.104
                    date_obj = datetime.strptime(
                        request.get("session_time"), "%Y-%m-%d"
                    ).date()
                    session_time = datetime.combine(date_obj, time(17, 20))
                case "CS 412 C2":
                    latitude = 42.349
                    longitude = -71.104
                    date_obj = datetime.strptime(
                        request.get("session_time"), "%Y-%m-%d"
                    ).date()
                    session_time = datetime.combine(date_obj, time(18, 25))
                case "CS 412 C3":
                    latitude = 42.350
                    longitude = -71.105
                    date_obj = datetime.strptime(
                        request.get("session_time"), "%Y-%m-%d"
                    ).date()
                    session_time = datetime.combine(date_obj, time(19, 30))
                case _:
                    return "Something's wrong"
            form.instance.answer = request.get("answer")
            form.instance.name = class_chosen
            form.instance.latitude = latitude
            form.instance.longitude = longitude
            form.instance.session_time = session_time

            return super().form_valid(form)
