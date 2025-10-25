# File: mini_insta/views.py
# Author: Yihang Duanmu (harrydm@bu.edu), 10/16/2025
# Description: Views for the mini_insta application

from django.db.models.base import Model as Model
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .forms import *
from .models import *


class ProfileRequiredMixin(LoginRequiredMixin):
    """
    Require that a user be logged in before they can do anything that would modify the database
    """

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        user_profile = Profile.objects.get(user=self.request.user)
        is_following = (
            profile.get_followers().filter(follower_profile=user_profile).exists()
        )
        context["is_following"] = is_following
        return context


class LoggedInProfileDetailView(DetailView):
    """Define a view class to show one profile"""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


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


class CreatePostView(ProfileRequiredMixin, CreateView):
    """A view to handle creation of a new Comment on an Article"""

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_success_url(self):
        """Provide a URL to redirect to after creating a new Post"""

        # create and return a URL
        return reverse("show_logged_in_profile")

    def get_context_data(self):
        """Return the dictionary of context vatiables for use in the template"""

        context = super().get_context_data()

        # provide profile as a context
        profile = Profile.objects.get(user=self.request.user)
        context["profile"] = profile

        return context

    def form_valid(self, form):
        """This method handles the form submission and saves the new object to the Django database"""

        # retrieve the PK from the URL pattern
        profile = Profile.objects.get(user=self.request.user)
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


class UpdateProfileView(ProfileRequiredMixin, UpdateView):
    """View class to handle update of a profile based on its PK"""

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class UpdatePostView(ProfileRequiredMixin, UpdateView):
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


class DeletePostView(ProfileRequiredMixin, DeleteView):
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


class PostFeedListView(ProfileRequiredMixin, ListView):
    """Define a view class to show post feed of a profile"""

    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        """Return the set of posts for post feed"""

        queryset = super().get_queryset()

        profile = Profile.objects.get(user=self.request.user)
        queryset = profile.get_post_feed()
        return queryset

    def get_context_data(self, **kwargs):
        """Return the dictionary of context vatiable for use in the template"""

        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)

        # provide profile as context
        context["profile"] = profile

        # provide number of feed posts as context
        context["numPosts"] = self.get_queryset().count()

        return context


class SearchView(ProfileRequiredMixin, ListView):
    """Define a view class to provide search on profiles and posts"""

    model = Post
    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        """called first to dispatch (handle) any request"""
        response = super().dispatch(request, *args, **kwargs)

        # redirect if user is not logged in
        if getattr(response, "status_code", None) in (301, 302):
            return response

        # check for query
        if "query" not in self.request.GET:
            # return search.html if query is absent
            profile = Profile.objects.get(user=self.request.user)
            template_name = "mini_insta/search.html"
            return render(request, template_name, {"profile": profile})
        else:
            return response

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
        profile = Profile.objects.get(user=self.request.user)

        # provide profile as context
        context["profile"] = profile

        # provide query as context
        query = self.request.GET.get("query", "")
        if query:
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


def logout(request):
    """Return the logout page"""
    template_name = "mini_insta/logout.html"

    return render(request, template_name)


class CreateProfileView(CreateView):
    """A view to create a new profile for a new User"""

    template_name = "mini_insta/create_profile_form.html"
    form_class = CreateProfileForm
    model = Profile

    def get_context_data(self, **kwargs):
        """Return the dictionary of context vatiables for use in the template"""

        context = super().get_context_data(**kwargs)

        registrationForm = UserCreationForm

        # provide the user creation form as context
        context["register"] = registrationForm

        # account for errors in registering
        if "user_form" in kwargs:
            context["register"] = kwargs["user_form"]
            print(context["register"])

        return context

    def form_valid(self, form):
        """This method handles the form submission and saves the new object to the Django database"""

        # Create a new user form from POST data
        if self.request.POST:
            print(self.request.POST.getlist("username"))
            user_form = UserCreationForm(
                {
                    "username": self.request.POST.getlist("username")[0],
                    "password1": self.request.POST.get("password1"),
                    "password2": self.request.POST.get("password2"),
                }
            )
            if user_form.is_valid():
                user = user_form.save()
                # Log the user
                login(
                    self.request,
                    user,
                    backend="django.contrib.auth.backends.ModelBackend",
                )

                # Link the profile to this new user
                form.instance.user = user

                return super().form_valid(form)
            # User form invalid — render same page with errors
        return self.render_to_response(
            self.get_context_data(
                form=form, register=user_form, errors=user_form.errors
            )
        )

    def get_success_url(self):
        """The url to redirect to after creating a new User"""

        return reverse("show_logged_in_profile")


class CreateFollowView(LoginRequiredMixin, View):
    """Create a Follow relationship between logged-in user and another profile"""

    def dispatch(self, request, *args, **kwargs):
        # Get the profile to follow
        profile_to_follow = Profile.objects.get(pk=kwargs["pk"])

        # Get logged-in user's profile
        logged_in_profile = Profile.objects.get(user=request.user)

        if logged_in_profile != profile_to_follow:
            # Create Follow object (use get_or_create to avoid duplicates)
            Follow.objects.get_or_create(
                profile=profile_to_follow,
                follower_profile=logged_in_profile,
            )

        # Redirect back to the profile page
        return redirect("show_profile", pk=profile_to_follow.pk)


class DeleeFollowView(LoginRequiredMixin, View):
    """Delete a Follow relationship between logged-in user and another profile"""

    def dispatch(self, request, *args, **kwargs):
        # Get the profile to follow
        profile_to_unfollow = Profile.objects.get(pk=kwargs["pk"])

        # Get logged-in user's profile
        logged_in_profile = Profile.objects.get(user=request.user)

        if logged_in_profile != profile_to_unfollow:
            # Create Follow object (use get_or_create to avoid duplicates)
            Follow.objects.filter(
                profile=profile_to_unfollow,
                follower_profile=logged_in_profile,
            ).delete()

        # Redirect back to the profile page
        return redirect("show_profile", pk=profile_to_unfollow.pk)
