from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random


# Create your views here.
def home(request):
    """Fund to respond to the "home" request."""

    response_text = """
    <html>
    <h1>Hello, world!</h1>
    </html>
    """

    return HttpResponse(response_text)


def home_page(request):
    """Respond to the URL, delegate work to a template"""
    template_name = "hw/home.html"
    context = {
        "time": time.ctime(),
    }
    return render(request, template_name, context)


def about(request):
    """Respond to the URL, delegate work to a template"""
    template_name = "hw/about.html"
    context = {
        "time": time.ctime(),
    }
    return render(request, template_name, context)
