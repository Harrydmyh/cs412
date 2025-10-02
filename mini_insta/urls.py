# mini-insta/urls.py
# urls for the mini-insta application

from django.urls import path
from .views import *

urlpatterns = [
    path("", ProfileListView.as_view(), name="show_all_profiles"),
    path("profile/<int:pk>", ProfileDetailView.as_view(), name="show_profile"),
    path("post/<int:pk>", PostDetailView.as_view(), name="show_post"),
]
