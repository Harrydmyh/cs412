# marathon_analytics/views.py
# Create your views here.
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from .models import Result


class ResultListView(ListView):
    """View to display marathon results"""

    model = Result
    template_name = "marathon_analytics/results.html"
    context_object_name = "results"
    paginate_by = 25

    def get_queryset(self):
        """limit the queryset"""
        results = super().get_queryset()
        # return results[:25]

        # look for URL parameters to filter by
        if "city" in self.request.GET:
            city = self.request.GET["city"]

            if city:
                results = results.filter(city=city)

        return results
