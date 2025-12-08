# attendance/urls.py
# urls for the attendance application
# Author: Yihang Duanmu (harrydm@bu.edu), 12/2/2025

from django.urls import path
from .views import *

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
]
