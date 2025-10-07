# blog/view.py
# views for the blog application
from django.db.models.base import Model as Model
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse
from .models import Article, Comment
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm
import random


# Create your views here.
class ShowAllView(ListView):
    """Define a view class to show all blog Articles"""

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"


class ArticleView(DetailView):
    """Display a single article"""

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"


class RandomArticleView(DetailView):
    """Display a single article selected at random"""

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"

    def get_object(self):
        """return one instance of the Article object selected at random"""

        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article


# define a subclass of CreateView to handle creation of Article objects
class CreateArticleView(CreateView):
    """A view to handle creation of a new Article
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Article object (POST)
    """

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def form_valid(self, form):
        """Override the default method to add some debug information"""

        # print out the form data
        print(f"CreateArticleView.form_valid(): {form.cleaned_data}")

        # delagate work to the superclass to do the rest:
        return super().form_valid(form)


class CreateCommentView(CreateView):
    """A view to handle creation of a new Comment on an Article"""

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_success_url(self):
        """Provide a URL to redirect to after creating a new Comment"""

        # create and return a URL
        pk = self.kwargs["pk"]
        return reverse("article", kwargs={"pk": pk})

    def get_context_data(self):
        """Return the dictionary of context vatiables for use in the template"""
        context = super().get_context_data()
        pk = self.kwargs["pk"]

        article = Article.objects.get(pk=pk)
        context["article"] = article

        return context

    def form_valid(self, form):
        """This method handles the form submission and saves the new object to the Django database"""

        print(form.cleaned_data)
        # retrieve the PK from the URL pattern
        pk = self.kwargs["pk"]
        article = Article.objects.get(pk=pk)
        form.instance.article = article

        return super().form_valid(form)


class UpdateArticleView(UpdateView):
    """View class to handle update of an article based on its PK"""

    model = Article
    form_class = UpdateArticleForm
    template_name = "blog/update_article_form.html"


class DeleteCommentView(DeleteView):
    """View class to delete a comment on an Article"""

    model = Comment
    template_name = "blog/delete_comment_form.html"

    def get_success_url(self) -> str:
        """Return the URL to redirect to after a successful delete"""

        # find the PK for this Comment
        pk = self.kwargs["pk"]
        # find the Comment object
        comment = Comment.objects.get(pk=pk)

        # find the PK of the Article to which this comment is associated
        article = comment.article

        # return the URL to redirect to
        return reverse("article", kwargs={"pk": article.pk})
