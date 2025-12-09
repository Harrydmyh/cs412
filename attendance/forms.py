# attendance/forms.py
# forms for the attendance application
# Author: Yihang Duanmu (harrydm@bu.edu), 12/2/2025

from django import forms
from .models import *


class CreateClassForm(forms.ModelForm):
    """A form to add a Class to the database"""

    class_name = forms.ChoiceField(
        choices=[
            ("CS 412 A1", "CS412 A1 - Lecture 9:30"),
            ("CS 412 B1", "CS412 B2 - Lecture 11:00"),
            ("CS 412 C1", "CS412 C1 - Discussion 12:20"),
            ("CS 412 C2", "CS412 C2 - Discussion 13:25"),
            ("CS 412 C3", "CS412 C3 - Discussion 14:30"),
        ],
        label="Class Name",
    )

    # Dropdown for answer (1 to 10)
    answer = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 11)],
        label="Choose an Answer for Students",
    )

    class Meta:
        """associate this form with a model from our database"""

        model = Class
        fields = ["session_time"]
        labels = {
            "session_time": "Class date",
        }
        widgets = {
            "session_time": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }


class CreateProfileForm(forms.ModelForm):
    """A form to add a Profile to the database"""

    class Meta:
        """associate this form with a model from our database"""

        model = Profile
        fields = ["first_name", "last_name", "lecture", "discussion"]
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "Lecture": "Your Lecture Session",
            "Discussion": "Your Discussion Session",
        }
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "size": 30,
                    "class": "form-control",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "size": 30,
                }
            ),
            "lecture": forms.Select(
                choices=[
                    ("CS 412 A1", "CS 412 A1"),
                    ("CS 412 B1", "CS 412 B1"),
                ]
            ),
            "discussion": forms.Select(
                choices=[
                    ("CS 412 C1", "CS 412 C1"),
                    ("CS 412 C2", "CS 412 C2"),
                    ("CS 412 C3", "CS 412 C3"),
                ]
            ),
        }
