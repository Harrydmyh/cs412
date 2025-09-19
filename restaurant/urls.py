# File: restaurant/urls.py
# Author: Yihang Duanmu (harrydm@bu.edu), 9/16/2025
# Description: URL patterns for the restaurant application

from django.urls import path
from django.conf import settings
from . import views

# URL patterns specific to the hw app:
urlpatterns = [
    path("main/", views.main, name="main_page"),
    path("order/", views.order, name="order_page"),
    path("confirmation/", views.confirmation, name="confirmation_page"),
]
