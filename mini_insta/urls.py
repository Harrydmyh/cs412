# mini-insta/urls.py
# urls for the mini-insta application
# Author: Yihang Duanmu (harrydm@bu.edu), 10/16/2025

from django.urls import path
from . import views
from .views import *

# generic view for authentication/authorization
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", ProfileListView.as_view(), name="show_all_profiles"),
    path("profile/<int:pk>", ProfileDetailView.as_view(), name="show_profile"),
    path("profile", LoggedInProfileDetailView.as_view(), name="show_logged_in_profile"),
    path("post/<int:pk>", PostDetailView.as_view(), name="show_post"),
    path("profile/create_post", CreatePostView.as_view(), name="create_post"),
    path(
        "profile/update",
        UpdateProfileView.as_view(),
        name="update_profile",
    ),
    path(
        "post/<int:pk>/delete",
        DeletePostView.as_view(),
        name="delete_post",
    ),
    path(
        "post/<int:pk>/update",
        UpdatePostView.as_view(),
        name="update_post",
    ),
    path(
        "profile/<int:pk>/followers",
        ShowFollowersDetailView.as_view(),
        name="show_followers",
    ),
    path(
        "profile/<int:pk>/following",
        ShowFollowingDetailView.as_view(),
        name="show_following",
    ),
    path(
        "profile/feed",
        PostFeedListView.as_view(),
        name="show_feed",
    ),
    path(
        "profile/search",
        SearchView.as_view(),
        name="search",
    ),
    path(
        "login",
        auth_views.LoginView.as_view(template_name="mini_insta/login.html"),
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
    path(
        "create_profile",
        CreateProfileView.as_view(),
        name="create_profile",
    ),
    path(
        "profile/<int:pk>/follow",
        CreateFollowView.as_view(),
        name="create_follow",
    ),
    path(
        "profile/<int:pk>/delete_follow",
        DeleteFollowView.as_view(),
        name="delete_follow",
    ),
    path(
        "post/<int:pk>/like",
        CreateLikeView.as_view(),
        name="create_like",
    ),
    path(
        "post/<int:pk>/delete_like",
        DeleteLikeView.as_view(),
        name="delete_like",
    ),
]
