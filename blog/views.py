# blog/view.py
# views for the blog application
from django.db.models.base import Model as Model
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from .models import Article
from .forms import CreateArticleForm, CreateCommentForm
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
