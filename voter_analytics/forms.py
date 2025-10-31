# voter_analytics/forms.py
# forms for creating post in the voter analytics application
# Author: Yihang Duanmu (harrydm@bu.edu), 10/30/2025

from django import forms
from datetime import date


class VoterSearchForm(forms.Form):
    # choices for the fields
    PARTY_CHOICES = [
        ("", "-- Select Party --"),
        ("A ", "A"),
        ("AA", "AA"),
        ("CC", "CC"),
        ("D ", "D"),
        ("E ", "E"),
        ("EE", "EE"),
        ("FF", "FF"),
        ("G ", "G"),
        ("GG", "GG"),
        ("H ", "H"),
        ("HH", "HH"),
        ("J ", "J"),
        ("K ", "K"),
        ("L ", "L"),
        ("O ", "O"),
        ("P ", "P"),
        ("Q ", "Q"),
        ("R ", "R"),
        ("S ", "S"),
        ("T ", "T"),
        ("U ", "U"),
        ("V ", "V"),
        ("W ", "W"),
        ("X ", "X"),
        ("Y ", "Y"),
        ("Z ", "Z"),
    ]

    SCORE_CHOICES = [("", "-- Select Score --")] + [(i, str(i)) for i in range(6)]

    current_year = date.today().year
    YEAR_CHOICES = [("", "-- Select Year --")] + [
        (y, y) for y in range(current_year, 1899, -1)
    ]

    # fields of the form
    party_affiliation = forms.ChoiceField(choices=PARTY_CHOICES, required=False)
    min_dob = forms.ChoiceField(choices=YEAR_CHOICES, required=False)
    max_dob = forms.ChoiceField(choices=YEAR_CHOICES, required=False)
    voter_score = forms.ChoiceField(choices=SCORE_CHOICES, required=False)

    v20state = forms.BooleanField(required=False, label="2020 State")
    v21town = forms.BooleanField(required=False, label="2021 Town")
    v21primary = forms.BooleanField(required=False, label="2021 Primary")
    v22general = forms.BooleanField(required=False, label="2022 General")
    v23town = forms.BooleanField(required=False, label="2023 Town")
