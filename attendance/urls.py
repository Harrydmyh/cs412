# attendance/urls.py
# urls for the attendance application
# Author: Yihang Duanmu (harrydm@bu.edu), 12/2/2025

from django.urls import path
from . import views
from .views import *

# generic view for authentication/authorization
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("profile/<int:pk>", ProfileView.as_view(), name="profile_page"),
    path("signin/<int:pk>", SigninView.as_view(), name="signin"),
    path(
        "profile/<int:pk>/create_class", CreateClassView.as_view(), name="create_class"
    ),
    path(
        "profile/<int:pk>/show_all_classes",
        ShowAllClassesView.as_view(),
        name="show_all_classes",
    ),
    path(
        "profile/<int:profile_pk>/class/<int:pk>/delete/",
        DeleteClassView.as_view(),
        name="delete_class",
    ),
    path(
        "profile/<int:pk>/student_attendance",
        ShowStudentsInClassView.as_view(),
        name="student_attendance",
    ),
    path(
        "profile/<int:pk>/attendance",
        ShowStudentAttendence.as_view(),
        name="attendance",
    ),
    path(
        "login",
        auth_views.LoginView.as_view(template_name="attendance/login.html"),
        name="login",
    ),
    path(
        "logout",
        auth_views.LogoutView.as_view(next_page="logout_confirmation"),
        name="logout",
    ),
    path(
        "loggedout",
        views.logout,
        name="logout_confirmation",
    ),
    path("my-profile/", redirect_to_my_profile, name="my_profile"),
]
