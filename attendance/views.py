# attendance/views.py
# views for the attendance application
# Author: Yihang Duanmu (harrydm@bu.edu), 12/2/2025

from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, DeleteView
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
        return reverse("profile_page", kwargs={"pk": self.kwargs["pk"]})

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
                    session_time = datetime.combine(date_obj, time(9, 30))
                case "CS 412 B1":
                    latitude = 42.350
                    longitude = -71.103
                    date_obj = datetime.strptime(
                        request.get("session_time"), "%Y-%m-%d"
                    ).date()
                    session_time = datetime.combine(date_obj, time(11, 0))
                case "CS 412 C1":
                    latitude = 42.349
                    longitude = -71.104
                    date_obj = datetime.strptime(
                        request.get("session_time"), "%Y-%m-%d"
                    ).date()
                    session_time = datetime.combine(date_obj, time(12, 20))
                case "CS 412 C2":
                    latitude = 42.349
                    longitude = -71.104
                    date_obj = datetime.strptime(
                        request.get("session_time"), "%Y-%m-%d"
                    ).date()
                    session_time = datetime.combine(date_obj, time(13, 25))
                case "CS 412 C3":
                    latitude = 42.350
                    longitude = -71.105
                    date_obj = datetime.strptime(
                        request.get("session_time"), "%Y-%m-%d"
                    ).date()
                    session_time = datetime.combine(date_obj, time(14, 30))
                case _:
                    return "Something's wrong"
            form.instance.answer = request.get("answer")
            form.instance.name = class_chosen
            form.instance.latitude = latitude
            form.instance.longitude = longitude
            form.instance.session_time = session_time

            return super().form_valid(form)


class ShowAllClassesView(DetailView):
    """A view to show the list of classes for instructors"""

    model = Profile
    template_name = "attendance/show_all_classes.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        """Return the dictionary of context vatiable for use in the template"""

        context = super().get_context_data(**kwargs)
        context["classes"] = Class.objects.order_by("-session_time")
        return context


class DeleteClassView(DeleteView):
    """View class to handle delete of a class based on its PK"""

    model = Class
    template_name = "attendance/delete_class_form.html"
    context_object_name = "class"

    def get_context_data(self, **kwargs):
        """Return the dictionary of context variables for use in the template"""
        context = super().get_context_data(**kwargs)
        profile_pk = self.kwargs["profile_pk"]
        profile = Profile.objects.get(pk=profile_pk)
        context["profile"] = profile
        return context

    def get_success_url(self):
        """Provide a URL to redirect to after deleting a Post"""
        profile_pk = self.kwargs["profile_pk"]
        return reverse("show_all_classes", kwargs={"pk": profile_pk})


class ShowStudentsInClassView(ListView):
    """View students attendance to classes"""

    model = Profile
    template_name = "attendance/students_attend_classes.html"
    context_object_name = "records"
    paginate_by = 20

    def get_queryset(self):
        """handle searching for records"""
        records = super().get_queryset()
        records = records.filter(is_instructor=False)
        return records


class ShowStudentAttendence(ListView):
    """Student view of attendance to classes"""

    model = Profile
    template_name = "attendance/students_attendance.html"
    context_object_name = "records"
    paginate_by = 20

    def get_queryset(self):
        """handle searching for records"""
        records = super().get_queryset()
        student = Profile.objects.get(pk=self.kwargs["pk"])
        records = Class.objects.filter(
            Q(name=student.lecture) | Q(name=student.discussion)
        )
        return records

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = Profile.objects.get(pk=self.kwargs["pk"])
        context["profile"] = student
        for r in context["records"]:
            r.attend_record = Attend.objects.filter(student=student, session=r).first()
        return context
