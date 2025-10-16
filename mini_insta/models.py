# mini-insta/models.py
# model for the mini-insta application
# Author: Yihang Duanmu (harrydm@bu.edu), 10/16/2025

from django.db import models
from django.urls import reverse


# Create your models here.
class Profile(models.Model):
    """Encapsulate the data of the profile of an individual user"""

    # define the data attributes of the Profile object
    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    profile_image_url = models.URLField(blank=False)
    bio_text = models.TextField(blank=True)
    join_date = models.DateField(blank=False)

    def __str__(self) -> str:
        """return a string representation of this model instance"""
        return f"{self.display_name}"

    def get_all_posts(self):
        """Return a QuerySet of comments about this profile"""

        # use the object manager to retrieve posts
        posts = Post.objects.filter(profile=self)
        return posts

    def get_num_posts(self):
        """Return the number of posts for a profile"""

        posts = Post.objects.filter(profile=self)
        return len(posts)

    def get_followers(self):
        """Return a QuerySet of followers of this profile"""

        # use the object manager to retrieve followers
        followers = Follow.objects.filter(profile=self)
        return followers

    def get_num_followers(self):
        """Return the number of followers for a profile"""

        followers = Follow.objects.filter(profile=self)
        return len(followers)

    def get_following(self):
        """Return a QuerySet of followers of this profile"""

        # use the object manager to retrieve following
        following = Follow.objects.filter(follower_profile=self)
        return following

    def get_num_following(self):
        """Return the number of followers for a profile"""

        following = Follow.objects.filter(follower_profile=self)
        return len(following)

    def get_absolute_url(self):
        """Provide a URL to redirect to after updating a profile"""

        # create and return a URL
        pk = self.pk
        return reverse("show_profile", kwargs={"pk": pk})


class Post(models.Model):
    """Encapsulate the data of a post by an individual user"""

    # define the data attributes of the Profile object
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=False)

    def __str__(self) -> str:
        """return a string representation of this model instance"""
        return f"Comment by {self.profile.display_name} on {self.timestamp}"

    def get_absolute_url(self):
        """Provide a URL to redirect to after updating a profile"""

        # create and return a URL
        pk = self.pk
        return reverse("show_post", kwargs={"pk": pk})

    def get_all_photos(self):
        """Return a QuerySet of comments about this post"""

        # use the object manager to retrieve comments
        photos = Photo.objects.filter(post=self)
        return photos


class Photo(models.Model):
    """Encapsulate the data of an image associated to a post"""

    # define the data attributes of the Profile object
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """return a string representation of this model instance"""
        return f"Image for comment by {self.post.profile.display_name} on {self.post.timestamp}"

    def get_image_url(self):
        if self.image_file:
            return self.image_file.url
        else:
            return self.image_url


class Follow(models.Model):
    """Encapsulate the data of a profile associated to another profile"""

    # define the data attributes of the Profile object
    profile = models.ForeignKey(
        Profile, related_name="profile", on_delete=models.CASCADE
    )
    follower_profile = models.ForeignKey(
        Profile, related_name="follower_profile", on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """return a string representation of this model instance"""
        return (
            f"{self.follower_profile.display_name} follows {self.profile.display_name}"
        )
