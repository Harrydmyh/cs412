# attendance/views.py
# views for the attendance application
# Author: Yihang Duanmu (harrydm@bu.edu), 12/2/2025

from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView, View
from django.http import HttpResponse
from .models import *
from .forms import *
from datetime import datetime, time
from django.contrib.auth.mixins import LoginRequiredMixin
import csv


class RoleRequiredMixin(LoginRequiredMixin):
    """A parent mixin for custom user requirements"""

    login_url = "login"
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
    """A mixin to require user be an instructor"""

    required_role = "instructor"


class StudentRequiredMixin(RoleRequiredMixin):
    """A mixin to require user be a student"""

    required_role = "student"


class UserRequiredMixin(RoleRequiredMixin):
    """A mixin to require user be logged in"""

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
        """Get the profile associated with the current user"""
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
            # Assign location and session to chosen class
            if class_chosen == "CS 412 A1":
                latitude = 42.350
                longitude = -71.103
                date_obj = datetime.strptime(
                    request.get("session_time"), "%Y-%m-%d"
                ).date()
                session_time = datetime.combine(date_obj, time(9, 30))

            elif class_chosen == "CS 412 B1":
                latitude = 42.350
                longitude = -71.103
                date_obj = datetime.strptime(
                    request.get("session_time"), "%Y-%m-%d"
                ).date()
                session_time = datetime.combine(date_obj, time(11, 0))

            elif class_chosen == "CS 412 C1":
                latitude = 42.349
                longitude = -71.104
                date_obj = datetime.strptime(
                    request.get("session_time"), "%Y-%m-%d"
                ).date()
                session_time = datetime.combine(date_obj, time(12, 20))

            elif class_chosen == "CS 412 C2":
                latitude = 42.349
                longitude = -71.104
                date_obj = datetime.strptime(
                    request.get("session_time"), "%Y-%m-%d"
                ).date()
                session_time = datetime.combine(date_obj, time(13, 25))

            elif class_chosen == "CS 412 C3":
                latitude = 42.350
                longitude = -71.105
                date_obj = datetime.strptime(
                    request.get("session_time"), "%Y-%m-%d"
                ).date()
                session_time = datetime.combine(date_obj, time(14, 30))

            elif class_chosen == "Test - CS 412 A1":
                latitude = 42.350
                longitude = -71.103
                session_time = datetime.now()

            else:
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
        """Get the profile associated with the current user"""
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
        """Get the profile associated with the current user"""
        return Profile.objects.get(user=self.request.user)


class ShowStudentAttendence(StudentRequiredMixin, ListView):
    """Student view of attendance to classes"""

    model = Profile
    template_name = "attendance/students_attendance.html"
    context_object_name = "records"
    paginate_by = 20

    def get_object(self):
        """Get the profile associated with the current user"""
        return Profile.objects.get(user=self.request.user)

    def get_queryset(self):
        """handle searching for records"""
        records = super().get_queryset()
        student = Profile.objects.get(user=self.request.user)
        records = Class.objects.filter(
            Q(name=student.lecture)
            | Q(name=student.discussion)
            | Q(name="Test - CS 412 A1")
        )
        return records

    def get_context_data(self, **kwargs):
        """Return the dictionary of context variables for use in the template"""
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
    """Redirect to profile page"""
    return redirect("profile_page")


class CreateAttendView(LoginRequiredMixin, View):
    """Create an Attend relationship between logged-in user and a class"""

    def post(self, request, *args, **kwargs):
        """Handle post request from the template"""
        profile = Profile.objects.get(user=self.request.user)
        session = Class.objects.get(pk=self.kwargs["pk"])
        response = self.request.POST
        answer = response.get("answer")
        latitude = round(float(response.get("lat")), 3)
        longitude = round(float(response.get("lng")), 3)

        # Create attendance record
        if (
            answer == session.answer
            and session.latitude - 0.004 <= latitude <= session.latitude + 0.004
            and session.longitude - 0.004 <= longitude <= session.longitude + 0.004
        ):
            # correct answer and location
            Attend.objects.create(
                student=profile,
                session=session,
                answer=answer,
                latitude=latitude,
                longitude=longitude,
                status="attended",
            )
        else:
            # wrong answer or location
            Attend.objects.create(
                student=profile,
                session=session,
                answer=answer,
                latitude=latitude,
                longitude=longitude,
                status="submitted",
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
            Appeal.objects.create(
                student=profile, session=session, reason=reason, status="submitted"
            )

            return redirect("attendance")


class HandleAppealsView(InstructorRequiredMixin, ListView):
    """Instructor view to handle appeals"""

    model = Profile
    template_name = "attendance/handle_appeals.html"
    context_object_name = "appeals"

    def get_object(self):
        """Get the profile associated with the current user"""
        return Profile.objects.get(user=self.request.user)

    def get_queryset(self):
        """handle searching for records"""
        appeals = super().get_queryset()
        appeals = Appeal.objects.filter(status="submitted")
        return appeals


class ApproveView(InstructorRequiredMixin, View):
    """Approve an appeal and create a new attend relationship"""

    def dispatch(self, request, *args, **kwargs):
        """Override the dispatch method to add debugging information"""
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
            status="attended",
        )

        # Change appeal object
        appeal.status = "approved"
        appeal.save()

        # Redirect back to the profile page
        return redirect("handle_appeal")


class RejectView(InstructorRequiredMixin, View):
    """Reject an appeal and create a new attend relationship"""

    def dispatch(self, request, *args, **kwargs):
        """Override the dispatch method to add debugging information"""
        # Get the appeal object
        appeal = Appeal.objects.get(pk=kwargs["pk"])

        # Change appeal object
        appeal.status = "rejected"
        appeal.save()

        # Redirect back to the profile page
        return redirect("handle_appeal")


class CreateProfileView(CreateView):
    """A view to create a new profile for a new User"""

    template_name = "attendance/create_profile_form.html"
    form_class = CreateProfileForm
    model = Profile

    def get_context_data(self, **kwargs):
        """Return the dictionary of context vatiables for use in the template"""

        context = super().get_context_data(**kwargs)

        registrationForm = UserCreationForm

        # provide the user creation form as context
        context["register"] = registrationForm

        # account for errors in registering
        if "user_form" in kwargs:
            context["register"] = kwargs["user_form"]
            print(context["register"])

        return context

    def form_valid(self, form):
        """This method handles the form submission and saves the new object to the Django database"""

        # Create a new user form from POST data
        if self.request.POST:
            user_form = UserCreationForm(
                {
                    "username": self.request.POST.getlist("username")[0],
                    "password1": self.request.POST.get("password1"),
                    "password2": self.request.POST.get("password2"),
                }
            )
            if user_form.is_valid():
                user = user_form.save()
                # Log the user
                login(
                    self.request,
                    user,
                    backend="django.contrib.auth.backends.ModelBackend",
                )

                # Link the profile to this new user
                form.instance.user = user
                form.instance.is_instructor = False

                return super().form_valid(form)
            # User form invalid — render same page with errors
        return self.render_to_response(
            self.get_context_data(
                form=form, register=user_form, errors=user_form.errors
            )
        )

    def get_success_url(self):
        """The url to redirect to after creating a new User"""

        return reverse("profile_page")


def export_csv(request):
    """Export student participation to csv"""
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="attendance.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(
        [
            "Student Name",
            "Lecture Participation",
            "Discussion Participation",
            "Total Participation",
        ]
    )  # header row

    # Write rows from your database
    for student in Profile.objects.filter(is_instructor=False):
        writer.writerow(
            [
                f"{student.first_name} {student.last_name}",
                student.get_lecture_participation(),
                student.get_discussion_participation(),
                student.get_total_participation(),
            ]
        )

    return response
