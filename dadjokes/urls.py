# dadjokes/urls.py
# urls for the dadjokes application
# Author: Yihang Duanmu (harrydm@bu.edu), 11/11/2025

from django.urls import path
from .views import *

urlpatterns = [
    path("", ShowRandomView.as_view(), name="home"),
    path("random", ShowRandomView.as_view(), name="show_random"),
    path("jokes", ShowAllJokesView.as_view(), name="show_all_jokes"),
    path("joke/<int:pk>", ShowDetailJokeView.as_view(), name="show_detail_joke"),
    path("pictures", ShowAllPicturesView.as_view(), name="show_all_pictures"),
    path(
        "picture/<int:pk>", ShowDetailPictureView.as_view(), name="show_detail_picture"
    ),
    path("api/", JokeRandomAPIView.as_view(), name="home_api"),
    path("api/random", JokeRandomAPIView.as_view(), name="joke_random_api"),
    path("api/jokes", JokeListAPIView.as_view(), name="joke_list_api"),
    path("api/joke/<int:pk>", JokeDetailAPIView.as_view(), name="joke_detail_api"),
    path("api/pictures", PictureListAPIView.as_view(), name="picture_list_api"),
    path(
        "api/picture/<int:pk>",
        PictureDetailAPIView.as_view(),
        name="picture_detail_api",
    ),
]
