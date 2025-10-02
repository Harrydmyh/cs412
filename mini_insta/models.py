# mini-insta/models.py
# model for the mini-insta application
from django.db import models


# Create your models here.
class Profile(models.Model):
    """Encapsulate the data of the profile of an individual user"""

    # define the data attributes of the Profile object
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateField(blank=True)

    def __str__(self) -> str:
        """return a string representation of this model instance"""
        return f"{self.display_name}"

    def get_all_posts(self):
        """Return a QuerySet of comments about this post"""

        # use the object manager to retrieve comments
        posts = Post.objects.filter(profile=self)
        return posts


class Post(models.Model):
    """Encapsulate the data of a post by an individual user"""

    # define the data attributes of the Profile object
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=True)

    def __str__(self) -> str:
        """return a string representation of this model instance"""
        return f"Comment by {self.profile.display_name} on {self.timestamp}"

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
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """return a string representation of this model instance"""
        return f"Image for comment by {self.post.profile.display_name} on {self.post.timestamp}"
