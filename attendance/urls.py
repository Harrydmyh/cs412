# attendance/urls.py
# urls for the attendance application
# Author: Yihang Duanmu (harrydm@bu.edu), 12/2/2025

from django.urls import path
from . import views
from .views import *

# generic view for authentication/authorization
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("profile", ProfileView.as_view(), name="profile_page"),
    path("signin/<int:pk>", SigninView.as_view(), name="signin"),
    path("profile/create_class", CreateClassView.as_view(), name="create_class"),
    path(
        "profile/show_all_classes",
        ShowAllClassesView.as_view(),
        name="show_all_classes",
    ),
    path(
        "profile/class/<int:pk>/delete",
        DeleteClassView.as_view(),
        name="delete_class",
    ),
    path(
        "profile/student_attendance",
        ShowStudentsInClassView.as_view(),
        name="student_attendance",
    ),
    path(
        "profile/attendance",
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
    path(
        "profile/class/<int:pk>/attend",
        CreateAttendView.as_view(),
        name="mark_attendance",
    ),
    path(
        "profile/class/<int:pk>/appeal",
        AppealView.as_view(),
        name="appeal",
    ),
    path(
        "profile/handle_appeal",
        HandleAppealsView.as_view(),
        name="handle_appeal",
    ),
    path(
        "profile/<int:pk>/approve",
        ApproveView.as_view(),
        name="approve",
    ),
    path(
        "profile/<int:pk>/reject",
        RejectView.as_view(),
        name="reject",
    ),
    path(
        "create_profile",
        CreateProfileView.as_view(),
        name="create_profile",
    ),
    path(
        "export_csv",
        views.export_csv,
        name="export_csv",
    ),
]
