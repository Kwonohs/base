from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView

# Create your views here.
# def index(request):
#     posts = Post.objects.all()
#     return render(
#         request,
#         "news/index.html",
#         {
#             "posts": posts,
#         }
#     )


class PostList(ListView):
    model = Post
    ordering = '-pk'


class PostDetail(DetailView):
    model = Post
    