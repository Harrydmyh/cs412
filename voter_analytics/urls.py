# voter_analytics/urls.py
# urls for the voter analytics application
# Author: Yihang Duanmu (harrydm@bu.edu), 10/28/2025

from django.urls import path
from . import views

urlpatterns = [
    # map the URL (empty string) to the view
    path("", views.VoterListView.as_view(), name="voters"),
    path("voter/<int:pk>", views.VoterDetailView.as_view(), name="voter"),
    path("graphs", views.GraphListView.as_view(), name="graphs"),
]
