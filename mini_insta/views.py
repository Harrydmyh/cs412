# File: mini_insta/views.py
# Author: Yihang Duanmu (harrydm@bu.edu), 10/16/2025
# Description: Views for the mini_insta application

from typing import Any
from django.db.models.base import Model as Model
from django.urls import reverse
from django.shortcuts import render
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

    def get_context_data(self, **kwargs):
        """Return the dictionary of context vatiable for use in the template"""

        context = super().get_context_data(**kwargs)

        pk = self.kwargs["pk"]
        post = Post.objects.get(pk=pk)
        profile = post.profile

        # provide profile as context
        context["profile"] = profile

        return context


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

        # provide profile as a context
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

        # include the images
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

    def get_context_data(self, **kwargs):
        """Return the dictionary of context vatiable for use in the template"""

        context = super().get_context_data(**kwargs)

        pk = self.kwargs["pk"]
        post = Post.objects.get(pk=pk)
        profile = post.profile

        # provide profile as context
        context["profile"] = profile

        return context


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

        # provide post and profile as context
        context["post"] = post
        context["profile"] = profile

        return context

    def get_success_url(self):
        """Provide a URL to redirect to after deleting a Post"""

        # create and return a URL
        pk = self.kwargs["pk"]
        profile_pk = Post.objects.get(pk=pk).profile.pk
        return reverse("show_profile", kwargs={"pk": profile_pk})


class ShowFollowersDetailView(DetailView):
    """Define a view class to show profiles of followers"""

    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"


class ShowFollowingDetailView(DetailView):
    """Define a view class to show profiles of following"""

    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"


class PostFeedListView(ListView):
    """Define a view class to show post feed of a profile"""

    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        """Return the set of posts for post feed"""

        queryset = super().get_queryset()

        pk = self.kwargs["pk"]
        profile = Profile.objects.get(pk=pk)
        queryset = profile.get_post_feed()
        return queryset

    def get_context_data(self, **kwargs):
        """Return the dictionary of context vatiable for use in the template"""

        context = super().get_context_data(**kwargs)

        pk = self.kwargs["pk"]
        profile = Profile.objects.get(pk=pk)

        # provide profile as context
        context["profile"] = profile

        # provide number of feed posts as context
        context["numPosts"] = self.get_queryset().count()

        return context


class SearchView(ListView):
    """Define a view class to provide search on profiles and posts"""

    model = Post
    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        """called first to dispatch (handle) any request"""

        # check for query
        if "query" not in self.request.GET:
            # return search.html if query is absent
            profile_pk = self.kwargs.get("pk")
            profile = Profile.objects.get(pk=profile_pk)
            template_name = "mini_insta/search.html"
            return render(request, template_name, {"profile": profile})
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Return the set of posts for post feed"""

        queryset = super().get_queryset()

        if self.request.GET:
            query = self.request.GET["query"]
            print(query)
            if query == "":
                queryset = Post.objects.none()
            else:
                queryset = Post.objects.filter(caption__contains=query)

        return queryset

    def get_context_data(self, **kwargs):
        """Return the dictionary of context vatiable for use in the template"""

        context = super().get_context_data(**kwargs)

        pk = self.kwargs["pk"]
        profile = Profile.objects.get(pk=pk)

        # provide profile as context
        context["profile"] = profile

        # provide query as context
        query = self.request.GET["query"]
        context["query"] = query

        # provide posts that match the query as context
        posts = self.get_queryset()
        context["posts"] = posts

        if query == "":
            profiles = Profile.objects.none()
        else:
            profiles = (
                Profile.objects.filter(username__contains=query)
                | Profile.objects.filter(display_name__contains=query)
                | Profile.objects.filter(bio_text__contains=query)
            )

        # provide profiles that match the query as context
        context["profiles"] = profiles

        # provide number of result profiles and posts as context
        context["numProfiles"] = profiles.count()
        context["numPosts"] = posts.count()

        return context
