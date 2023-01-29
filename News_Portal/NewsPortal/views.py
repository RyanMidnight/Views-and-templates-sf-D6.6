from django.views.generic import ListView, DetailView
from .models import Post


class PostsList(ListView):
    model = Post
    ordering = '-pub_date'
    template_name = 'news_list.html'
    context_object_name = 'posts'


class PostDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'post'
