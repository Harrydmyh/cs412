# voter_analytics/views.py
# views for the voter analytics application
# Author: Yihang Duanmu (harrydm@bu.edu), 10/28/2025

from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from .models import Voter


class RecordListView(ListView):
    """View to display voter records"""

    model = Voter
    template_name = "voter_analytics/records.html"
    context_object_name = "records"
    paginate_by = 25

    # def get_queryset(self):
    #     """limit the queryset"""
    #     results = super().get_queryset()
    #     # return results[:25]

    #     # look for URL parameters to filter by
    #     if "city" in self.request.GET:
    #         city = self.request.GET["city"]

    #         if city:
    #             results = results.filter(city=city)

    #     return results
