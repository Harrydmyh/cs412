# attendance/views.py
# views for the attendance application
# Author: Yihang Duanmu (harrydm@bu.edu), 12/2/2025

from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView, View
from .models import *
from .forms import *
from datetime import datetime, time
from django.contrib.auth.mixins import LoginRequiredMixin


class RoleRequiredMixin(LoginRequiredMixin):
    login_url = "/attendance/login"
    required_role = None  # "instructor", "student", or None for any user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return super().handle_no_permission()

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return self.handle_no_permission()

        # Ensure the user has a profile
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return self.handle_no_permission()

        # Role validation
        if self.required_role == "instructor" and not profile.is_instructor:
            return self.handle_no_permission()

        if self.required_role == "student" and profile.is_instructor:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class InstructorRequiredMixin(RoleRequiredMixin):
    required_role = "instructor"


class StudentRequiredMixin(RoleRequiredMixin):
    required_role = "student"


class UserRequiredMixin(RoleRequiredMixin):
    required_role = None


# Create your views here.
class ProfileView(UserRequiredMixin, DetailView):
    """A view to show home page for students and instructor"""

    model = Profile
    template_name = "attendance/home.html"
    context_object_name = "profile"

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class SigninView(StudentRequiredMixin, DetailView):
    """A view to show signin page for students"""

    model = Class
    template_name = "attendance/signin.html"
    context_object_name = "class"

    def get_context_data(self, **kwargs):
        """Return the dictionary of context variables for use in the template"""
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(user=self.request.user)
        return context


class CreateClassView(InstructorRequiredMixin, CreateView):
    """A view to handle creation of a new Class"""

    model = Profile
    form_class = CreateClassForm
    context_object_name = "profile"
    template_name = "attendance/create_class_form.html"

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get_success_url(self):
        """Provide a URL to redirect to after creating a new Class"""

        # create and return a URL
        return reverse("profile_page")

    def form_valid(self, form):
        """This method handles the form submission and saves the new object to the Django database"""

        # Create a new user form from POST data
        if self.request.POST:
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


class ShowAllClassesView(InstructorRequiredMixin, DetailView):
    """A view to show the list of classes for instructors"""

    model = Profile
    template_name = "attendance/show_all_classes.html"
    context_object_name = "profile"

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        """Return the dictionary of context vatiable for use in the template"""

        context = super().get_context_data(**kwargs)
        context["classes"] = Class.objects.order_by("-session_time")
        return context


class DeleteClassView(InstructorRequiredMixin, DeleteView):
    """View class to handle delete of a class based on its PK"""

    model = Class
    template_name = "attendance/delete_class_form.html"
    context_object_name = "class"

    def get_context_data(self, **kwargs):
        """Return the dictionary of context variables for use in the template"""
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(user=self.request.user)
        return context

    def get_success_url(self):
        """Provide a URL to redirect to after deleting a Post"""
        return reverse("show_all_classes")


class ShowStudentsInClassView(InstructorRequiredMixin, ListView):
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

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class ShowStudentAttendence(StudentRequiredMixin, ListView):
    """Student view of attendance to classes"""

    model = Profile
    template_name = "attendance/students_attendance.html"
    context_object_name = "records"
    paginate_by = 20

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get_queryset(self):
        """handle searching for records"""
        records = super().get_queryset()
        student = Profile.objects.get(user=self.request.user)
        records = Class.objects.filter(
            Q(name=student.lecture) | Q(name=student.discussion)
        )
        return records

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = Profile.objects.get(user=self.request.user)
        context["profile"] = student
        for r in context["records"]:
            r.attend_record = Attend.objects.filter(student=student, session=r).first()
        for r in context["records"]:
            r.appeal_record = Appeal.objects.filter(student=student, session=r).first()
        return context


def logout(request):
    """Return the logout page"""
    template_name = "attendance/logout.html"

    return render(request, template_name)


def redirect_to_my_profile(request):
    return redirect("profile_page")


class CreateAttendView(LoginRequiredMixin, View):
    """Create a Attend relationship between logged-in user and a class"""

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        session = Class.objects.get(pk=self.kwargs["pk"])
        response = self.request.POST
        answer = response.get("answer")
        latitude = round(float(response.get("lat")), 3)
        longitude = round(float(response.get("lng")), 3)

        # Create attendance record
        if (
            answer == session.answer
            and session.latitude - 0.002 <= latitude <= session.latitude + 0.002
            and session.longitude - 0.002 <= longitude <= session.longitude + 0.002
        ):
            Attend.objects.create(
                student=profile,
                session=session,
                answer=answer,
                latitude=latitude,
                longitude=longitude,
            )

        return redirect("profile_page")


class AppealView(StudentRequiredMixin, DetailView):
    """View students attendance to classes"""

    model = Profile
    template_name = "attendance/appeal.html"
    context_object_name = "profile"

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["class"] = Class.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self, request, *args, **kwargs):
        """This method handles the form submission and saves the new object to the Django database"""

        # Create a new user form from POST data
        if self.request.POST:
            request = self.request.POST
            profile = Profile.objects.get(user=self.request.user)
            session = Class.objects.get(pk=self.kwargs["pk"])
            reason = request.get("reason")
            Appeal.objects.create(student=profile, session=session, reason=reason)

            return redirect("attendance")


class HandleAppealsView(InstructorRequiredMixin, ListView):
    """Instructor view to handle appeals"""

    model = Profile
    template_name = "attendance/handle_appeals.html"
    context_object_name = "appeals"
    paginate_by = 20

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get_queryset(self):
        """handle searching for records"""
        appeals = super().get_queryset()
        appeals = Appeal.objects.all()
        return appeals


class ApproveView(InstructorRequiredMixin, View):
    """Approve an appeal and create a new attend relationship"""

    def dispatch(self, request, *args, **kwargs):
        # Get the appeal object
        appeal = Appeal.objects.get(pk=kwargs["pk"])
        student = appeal.student
        session = appeal.session

        # Create new attendance
        Attend.objects.create(
            student=student,
            session=session,
            answer=session.answer,
            latitude=session.latitude,
            longitude=session.longitude,
        )

        # Delete appeal object
        appeal.delete()

        # Redirect back to the profile page
        return redirect("handle_appeal")


class RejectView(InstructorRequiredMixin, View):
    """Reject an appeal and create a new attend relationship"""

    def dispatch(self, request, *args, **kwargs):
        # Get the appeal object
        appeal = Appeal.objects.get(pk=kwargs["pk"])

        # Delete appeal object
        appeal.delete()

        # Redirect back to the profile page
        return redirect("handle_appeal")
