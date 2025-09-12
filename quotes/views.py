# File: urls.py
# Author: Yihang Duanmu (harrydm@bu.edu), 9/11/2025
# Description: Views for quote of the day application

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random
import time

# Quote lists
quotes = [
    "Remembering that you are going to die is the best way I know to avoid the trap of thinking you have something to lose. You are already naked. There is no reason not to follow your heart.",
    "Being the richest man in the cemetery doesn't matter to me. Going to bed at night saying we've done something wonderful... that's what matters to me.",
    "Your time is limited, so don't waste it living someone else's life.",
]

# Image lists
images = [
    "https://www.thefamouspeople.com/profiles/thumbs/steve-jobs-3.jpg",
    "https://tse3.mm.bing.net/th/id/OIP.5ePQ8Sjcx1HLvVjGPtAWpAHaE8?r=0&rs=1&pid=ImgDetMain",
    "https://d.newsweek.com/en/full/663518/steve-jobs.jpg",
]


# Create your views here.
def main(request):
    """generate one quote and one image at random"""
    template_name = "quote.html"

    # index to generate random quotes and images
    quote_num = random.randint(0, 2)
    image_num = random.randint(0, 2)

    context = {
        "quote": quotes[quote_num],
        "image": images[image_num],
        "time": time.ctime(),
    }
    return render(request, template_name, context)


def quote(request):
    """generate one quote and one image at random"""

    return main(request)


def show_all(request):
    """display all available quotes and images"""
    template_name = "show_all.html"

    context = {
        "quotes": quotes,
        "images": images,
        "time": time.ctime(),
    }

    return render(request, template_name, context)


def about(request):
    """display all available quotes and images"""
    template_name = "about.html"

    context = {
        "time": time.ctime(),
    }

    return render(request, template_name, context)
