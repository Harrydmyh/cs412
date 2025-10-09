# File: mini_insta/views.py
# Author: Yihang Duanmu (harrydm@bu.edu), 9/25/2025
# Description: Views for the mini_insta application

from django.db.models.base import Model as Model
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
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
            # image_url = self.request.POST["image_url"]
            # if image_url != "":
            #     Photo.objects.create(post=self.object, image_url=image_url)
            files = self.request.FILES.getlist("image_files")
            if len(files) != 0:
                for file in files:
                    Photo.objects.create(post=self.object, image_file=file)

        return response


class UpdateProfileView(UpdateView):
    """View class to handle update of a profile based on its PK"""

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"


class UpdatePostView(UpdateView):
    """View class to handle update of a post based on its PK"""

    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"


class DeletePostView(DeleteView):
    """View class to handle delete of a profile based on its PK"""

    model = Post
    template_name = "mini_insta/delete_post_form.html"

    def get_context_data(self, **kwargs):
        """Return the dictionary of context vatiables for use in the template"""

        context = super().get_context_data(**kwargs)

        pk = self.kwargs["pk"]

        post = Post.objects.get(pk=pk)
        profile = post.profile

        context["post"] = post
        context["profile"] = profile

        return context

    def get_success_url(self):
        """Provide a URL to redirect to after deleting a Post"""

        # create and return a URL
        pk = self.kwargs["pk"]
        profile_pk = Post.objects.get(pk=pk).profile.pk
        return reverse("show_profile", kwargs={"pk": profile_pk})
