from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from .models import Post, Category, Tag

# Create your views here.
# def index(reqeust):
#     posts = Post.objects.all().order_by('-pk')

#     return render(
#         reqeust,
#         "blog/index.html",
#         {
#             "posts": posts,
#         }
#     )


# def single_post_page(reqeust, pk):
#     post = Post.objects.get(pk=pk)

#     return render(
#         reqeust,
#         "blog/single_post_page.html",
#         {
#             "post": post,
#         }
#     )


def tag_page(reqeust, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    return render(
        reqeust,
        "blog/post_list.html",
        {
            "post_list": post_list,
            "categories": Category.objects.all(),
            "no_category_post_count": Post.objects.filter(category=None).count(),
            "tag": tag,
        }
    )

def category_page(reqeust, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        reqeust,
        "blog/post_list.html",
        {
            "post_list": post_list,
            "categories": Category.objects.all(),
            "no_category_post_count": Post.objects.filter(category=None).count(),
            "category": category,
        }
    )


class PostList(ListView):
    model = Post
    ordering = "-pk"

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()

        return context


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()

        return context

class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    
    def form_valid(self, form):
        current_user = self.request.user

        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user

            return super().form_valid(form)

    def handle_no_permission(self):
        return redirect('/blog/')


class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']

    template_name = 'blog/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied