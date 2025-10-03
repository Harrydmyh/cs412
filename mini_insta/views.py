# File: mini_insta/views.py
# Author: Yihang Duanmu (harrydm@bu.edu), 9/25/2025
# Description: Views for the mini_insta application

from django.db.models.base import Model as Model
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from .forms import *
from .models import *


# Create your views here.
class ProfileListView(ListView):
    """Define a view class to show all profiles"""

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"


class ProfileDetailView(DetailView):
    """Define a view class to show one profile"""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"


class PostDetailView(DetailView):
    """Define a view class to show one post"""

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"


class CreatePostView(CreateView):
    """A view to handle creation of a new Comment on an Article"""

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_success_url(self):
        """Provide a URL to redirect to after creating a new Post"""

        # create and return a URL
        pk = self.kwargs["pk"]
        return reverse("show_profile", kwargs={"pk": pk})

    def get_context_data(self):
        """Return the dictionary of context vatiables for use in the template"""

        context = super().get_context_data()

        pk = self.kwargs["pk"]

        profile = Profile.objects.get(pk=pk)
        context["profile"] = profile

        return context

    def form_valid(self, form):
        """This method handles the form submission and saves the new object to the Django database"""

        # retrieve the PK from the URL pattern
        pk = self.kwargs["pk"]
        profile = Profile.objects.get(pk=pk)
        form.instance.profile = profile

        response = super().form_valid(form)

        if self.request.POST:
            image_url = self.request.POST["image_url"]
            if image_url != "":
                Photo.objects.create(post=self.object, image_url=image_url)

        return response
