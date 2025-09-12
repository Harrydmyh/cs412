# File: urls.py
# Author: Yihang Duanmu (harrydm@bu.edu), 9/11/2025
# Description: URL patterns for quote of the day application

from django.urls import path
from django.conf import settings
from . import views

# URL patterns specific to the hw app:
urlpatterns = [
    path("", views.main, name="main_page"),
    path("/quote", views.quote, name="quote_page"),
    path("/show_all", views.show_all, name="show_all_page"),
    path("/about", views.about, name="about_page"),
]
