# attendance/admin.py
# admin setup for the attendance application
# Author: Yihang Duanmu (harrydm@bu.edu), 11/25/2025
from django.contrib import admin

# Register your models here.
from .models import Profile, Class, Attend, Appeal

admin.site.register(Profile)
admin.site.register(Class)
admin.site.register(Attend)
admin.site.register(Appeal)
