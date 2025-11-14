# dadjokes/views.py
# views for the dadjokes application
# Author: Yihang Duanmu (harrydm@bu.edu), 11/11/2025

from typing import Any
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
)
from .models import Joke, Picture
import random
from rest_framework import generics
from .serializers import *


# Create your views here.
class ShowRandomView(ListView):
    """A view to show a random joke and a random picture"""

    model = Joke
    template_name = "dadjokes/show_random.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        joke = list(Joke.objects.all())
        random_joke = random.choice(joke)
        context["joke"] = random_joke

        picture = list(Picture.objects.all())
        random_picture = random.choice(picture)
        context["picture"] = random_picture

        return context


class ShowAllJokesView(ListView):
    """A view to show all the jokes"""

    model = Joke
    template_name = "dadjokes/show_all_jokes.html"
    context_object_name = "jokes"


class ShowAllPicturesView(ListView):
    """A view to show all the pictures"""

    model = Picture
    template_name = "dadjokes/show_all_pictures.html"
    context_object_name = "pictures"


class ShowDetailJokeView(DetailView):
    """A view to show one joke"""

    model = Joke
    template_name = "dadjokes/show_detail_joke.html"
    context_object_name = "joke"


class ShowDetailPictureView(DetailView):
    """A view to show one picture"""

    model = Picture
    template_name = "dadjokes/show_detail_picture.html"
    context_object_name = "picture"


class JokeRandomAPIView(generics.ListCreateAPIView):
    """
    An API view to return a random Joke
    """

    def get_queryset(self):
        queryset = Joke.objects.all()
        joke = list(queryset)
        random_joke = random.choice(joke)
        queryset = queryset.filter(pk=random_joke.pk)
        return queryset

    serializer_class = JokeSerializer


class PictureRandomAPIView(generics.ListCreateAPIView):
    """
    An API view to return a random Picture
    """

    def get_queryset(self):
        queryset = Picture.objects.all()
        picture = list(queryset)
        random_picture = random.choice(picture)
        queryset = queryset.filter(pk=random_picture.pk)
        return queryset

    serializer_class = PictureSerializer


class JokeListAPIView(generics.ListCreateAPIView):
    """
    An API view to return a listing of Jokes
    """

    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class PictureListAPIView(generics.ListCreateAPIView):
    """
    An API view to return a listing of Pictures
    """

    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class JokeDetailAPIView(generics.ListCreateAPIView):
    """
    An API view to return a one specific joke
    """

    def get_queryset(self):
        queryset = Joke.objects.all()
        pk = self.kwargs["pk"]
        queryset = queryset.filter(pk=pk)
        return queryset

    serializer_class = JokeSerializer


class PictureDetailAPIView(generics.ListCreateAPIView):
    """
    An API view to return a one specific picture
    """

    def get_queryset(self):
        queryset = Picture.objects.all()
        pk = self.kwargs["pk"]
        queryset = queryset.filter(pk=pk)
        return queryset

    serializer_class = PictureSerializer
