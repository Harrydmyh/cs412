# voter_analytics/views.py
# views for the voter analytics application
# Author: Yihang Duanmu (harrydm@bu.edu), 10/28/2025

from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models.functions import ExtractYear
from django.db.models import Count
from .models import Voter
from .forms import VoterSearchForm
import plotly
import plotly.graph_objs as go


class VoterListView(ListView):
    """View to display voter records"""

    model = Voter
    template_name = "voter_analytics/records.html"
    context_object_name = "records"
    paginate_by = 100

    def get_queryset(self):
        """handle searching for records"""
        records = super().get_queryset()

        # look for URL parameters to filter by
        params = self.request.GET

        # filter party affiliation
        party_affiliation = params.get("party_affiliation")
        if party_affiliation:
            records = records.filter(party_affiliation=party_affiliation)

        # filter date of birth
        min_dob = params.get("min_dob")
        max_dob = params.get("max_dob")
        if min_dob:
            records = records.filter(date_of_birth__year__gte=min_dob)
        if max_dob:
            records = records.filter(date_of_birth__year__lte=max_dob)

        # filter voter score
        voter_score = params.get("voter_score")
        if voter_score:
            records = records.filter(voter_score=voter_score)

        # filter voter score
        elections = ["v20state", "v21town", "v21primary", "v22general", "v23town"]
        for election in elections:
            election_result = params.get(election)
            if election_result:
                if election_result == "on":
                    election_result = True
                records = records.filter(**{election: election_result})

        return records

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_form = VoterSearchForm(self.request.GET or None)
        context["search"] = search_form
        return context


class VoterDetailView(DetailView):
    """Display results for a single runner"""

    model = Voter
    context_object_name = "r"
    template_name = "voter_analytics/record_detail.html"


class GraphListView(ListView):
    """View to display summary graphs"""

    model = Voter
    template_name = "voter_analytics/graphs.html"
    context_object_name = "records"
    paginate_by = 100

    def get_queryset(self):
        """handle searching for records"""
        records = super().get_queryset()

        # look for URL parameters to filter by
        params = self.request.GET

        # filter party affiliation
        party_affiliation = params.get("party_affiliation")
        if party_affiliation:
            records = records.filter(party_affiliation=party_affiliation)

        # filter date of birth
        min_dob = params.get("min_dob")
        max_dob = params.get("max_dob")
        if min_dob:
            records = records.filter(date_of_birth__year__gte=min_dob)
        if max_dob:
            records = records.filter(date_of_birth__year__lte=max_dob)

        # filter voter score
        voter_score = params.get("voter_score")
        if voter_score:
            records = records.filter(voter_score=voter_score)

        # filter voter score
        elections = ["v20state", "v21town", "v21primary", "v22general", "v23town"]
        for election in elections:
            election_result = params.get(election)
            if election_result:
                if election_result == "on":
                    election_result = True
                records = records.filter(**{election: election_result})

        return records

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        # get the search form
        search_form = VoterSearchForm(self.request.GET or None)
        context["search"] = search_form

        # create a bar chart with distributions of the voters' birth date
        birth_years = (
            queryset.annotate(year=ExtractYear("date_of_birth"))
            .values("year")
            .annotate(count=Count("id"))
            .order_by("year")
        )

        years = [item["year"] for item in birth_years]
        counts = [item["count"] for item in birth_years]

        fig = go.Bar(x=years, y=counts, marker_color="lightblue")

        graph_div_birth_date = plotly.offline.plot(
            {
                "data": [fig],
                "layout_title_text": f"Voter distribution by Year of Birth n = {len(queryset.all())}",
            },
            auto_open=False,
            output_type="div",
        )
        context["graph_div_birth_date"] = graph_div_birth_date

        # create a pie chart with distributions of the voters' party affiliation
        party_affiliation = (
            queryset.values("party_affiliation")
            .annotate(count=Count("id"))
            .order_by("party_affiliation")
        )

        party = [item["party_affiliation"] for item in party_affiliation]
        counts = [item["count"] for item in party_affiliation]

        fig = go.Pie(labels=party, values=counts)

        graph_div_party_affiliation = plotly.offline.plot(
            {
                "data": [fig],
                "layout_title_text": f"Voter distribution by Party Affiliation n = {len(queryset.all())}",
            },
            auto_open=False,
            output_type="div",
        )
        context["graph_div_party_affiliation"] = graph_div_party_affiliation

        # create a bar chart with distributions of the voters' election record
        elections = ["v20state", "v21town", "v21primary", "v22general", "v23town"]
        counts = [len(queryset.filter(**{election: True})) for election in elections]

        fig = go.Bar(x=elections, y=counts, marker_color="lightblue")

        graph_div_elections = plotly.offline.plot(
            {
                "data": [fig],
                "layout_title_text": f"Voter distribution by Election n = {len(queryset.all())}",
            },
            auto_open=False,
            output_type="div",
        )
        context["graph_div_elections"] = graph_div_elections

        return context
