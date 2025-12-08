# attendance/models.py
# models for the attendance application
# Author: Yihang Duanmu (harrydm@bu.edu), 11/25/2025
from django.db import models
from django.utils import timezone
from datetime import timedelta


# Create your models here.
class Profile(models.Model):
    """Encapsulate the data of a user profile of the app"""

    # define the data attributes of the Profile object
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    email = models.TextField(blank=False)
    is_instructor = models.BooleanField(blank=False)
    lecture = models.TextField(blank=False)
    discussion = models.TextField(blank=False)

    def __str__(self) -> str:
        """return a string representation of this model instance"""
        status = "Instructor" if self.is_instructor else "Student"
        return f"{status} {self.first_name} {self.last_name}"

    def class_happening(self):
        now = timezone.now()
        time_window_start = now - timedelta(minutes=15)
        time_window_end = now + timedelta(minutes=15)

        classes = Class.objects.filter(
            session_time__gte=time_window_start, session_time__lte=time_window_end
        )
        if classes.exists():
            is_my_class = (
                classes.first().name == self.lecture
                or classes.first().name == self.discussion
            )
        return classes.exists() and is_my_class

    def get_class_happening(self):
        now = timezone.now()
        time_window_start = now - timedelta(minutes=15)
        time_window_end = now + timedelta(minutes=15)

        classes = Class.objects.filter(
            session_time__gte=time_window_start, session_time__lte=time_window_end
        ).first()
        return classes


class Class(models.Model):
    """Encapsulate the data of a class session"""

    # define the data attributes of the Class object
    session_time = models.DateTimeField(blank=False)
    name = models.TextField(blank=False)
    answer = models.TextField(blank=False)
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)

    def __str__(self) -> str:
        """return a string representation of this model instance"""
        return f"{self.name} at {self.session_time}"


class Attend(models.Model):
    """Encapsulate the relationship of student attending class"""

    # define the data attributes of the Attend object
    student = models.ForeignKey(
        Profile, related_name="attend_profile", on_delete=models.CASCADE
    )
    session = models.ForeignKey(
        Class, related_name="attend_class", on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now=True)
    answer = models.TextField(blank=False)
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)

    def __str__(self) -> str:
        """return a string representation of this model instance"""
        return f"Student {self.student.first_name} {self.student.last_name} attending {self.session.session_time} in {self.session.classroom}"


class Appeal(models.Model):
    """Encapsulate the relationship of student apealling for attendance"""

    # define the data attributes of the Attend object
    student = models.ForeignKey(
        Profile, related_name="appeal_profile", on_delete=models.CASCADE
    )
    session = models.ForeignKey(
        Class, related_name="appeal_class", on_delete=models.CASCADE
    )
    reason = models.TextField(blank=False)

    def __str__(self) -> str:
        """return a string representation of this model instance"""
        return f"Student {self.student.first_name} {self.student.last_name} appealing for {self.session.session_time} in {self.session.classroom}"
