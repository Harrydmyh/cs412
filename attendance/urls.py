# attendance/urls.py
# urls for the attendance application
# Author: Yihang Duanmu (harrydm@bu.edu), 12/2/2025

from django.urls import path
from .views import *

urlpatterns = [
    path("profile/<int:pk>", ProfileView.as_view(), name="home"),
    path("signin/<int:pk>", SigninView.as_view(), name="signin"),
    path(
        "profile/<int:pk>/create_class", CreateClassView.as_view(), name="create_class"
    ),
]
