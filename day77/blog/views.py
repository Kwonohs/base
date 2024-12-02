from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .models import Post, Category, Tag, Comment
from .forms import CommentForm
from django.db.models import Q

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


# Function to handle displaying posts by a specific tag
def tag_page(request, slug):
    # Retrieve the tag object based on the slug provided
    tag = Tag.objects.get(slug=slug)
    # Get all posts that are associated with the retrieved tag
    post_list = tag.post_set.all()

    # Render the 'post_list.html' template, passing the tag and post data along with other context
    return render(
        request,
        "blog/post_list.html",
        {
            "post_list": post_list,  # List of posts associated with the tag
            "categories": Category.objects.all(),  # All categories for the sidebar
            "no_category_post_count": Post.objects.filter(category=None).count(),  # Count of posts with no category
            "tag": tag,  # The current tag object
        }
    )


# Function to handle displaying posts by a specific category
def category_page(request, slug):
    # Check if the slug is for posts with no category
    if slug == 'no_category':
        category = '미분류'  # "Uncategorized" in Korean
        post_list = Post.objects.filter(category=None)  # Get posts with no category
    else:
        # Retrieve the category object based on the slug
        category = Category.objects.get(slug=slug)
        # Get all posts associated with the category
        post_list = Post.objects.filter(category=category)

    # Render the 'post_list.html' template, passing the category and post data along with other context
    return render(
        request,
        "blog/post_list.html",
        {
            "post_list": post_list,  # List of posts in the selected category
            "categories": Category.objects.all(),  # All categories for the sidebar
            "no_category_post_count": Post.objects.filter(category=None).count(),  # Count of posts with no category
            "category": category,  # The current category object
        }
    )


# Class-based view for displaying a list of posts
class PostList(ListView):
    model = Post
    ordering = "-pk"  # Display posts in reverse chronological order
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data: categories and count of uncategorized posts
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()

        return context


# Class-based view for displaying the detail of a specific post
class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data: categories and count of uncategorized posts
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm

        return context


# Class-based view for creating a new post
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    # Restrict post creation to superusers and staff members
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user

        # Ensure that only authenticated and authorized users can create posts
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user  # Assign the current user as the author of the post
            response = super().form_valid(form)

            # Retrieve the 'tags_str' from the POST data (tags as a string)
            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()  # Remove extra spaces
                tags_str = tags_str.replace(',', ';')  # Replace commas with semicolons
                tags = tags_str.split(';')  # Split the string into individual tags

                # Loop through the tags and associate them with the current post
                for tag in tags:
                    tag = tag.strip()  # Clean up any extra spaces around each tag
                    tag_obj = Tag.objects.filter(name=tag).first()  # Check if the tag already exists

                    if not tag_obj:
                        # Create a new tag if it doesn't exist
                        slug = slugify(tag, allow_unicode=True)
                        tag_obj = Tag.objects.create(name=tag, slug=slug)
                    
                    self.object.tags.add(tag_obj)  # Associate the tag with the post

            return response

    def handle_no_permission(self):
        # Redirect the user to the blog index page if they don't have permission
        return redirect('/blog/')


# Class-based view for updating an existing post
class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    template_name = 'blog/post_update_form.html'

    # Restrict post update to superusers, staff, or the author of the post
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied  # Raise permission denied if the user is not the author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # If the post has tags, prepare a default string for the tags field
        if self.object.tags.exists():
            tags = list()
            for tag in self.object.tags.all():
                tags.append(tag.name)
            
            context['tags_str_default'] = '; '.join(tags)  # Join tags with semicolons

        return context

    def form_valid(self, form):
        current_user = self.request.user

        # Ensure that only authenticated and authorized users can update posts
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user  # Ensure the author is still the current user
            response = super().form_valid(form)

            # Retrieve the 'tags_str' from the POST data (tags as a string)
            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()  # Remove extra spaces
                tags_str = tags_str.replace(',', ';')  # Replace commas with semicolons
                tags = tags_str.split(';')  # Split the string into individual tags

                # Loop through the tags and associate them with the current post
                for tag in tags:
                    tag = tag.strip()  # Clean up any extra spaces around each tag
                    tag_obj = Tag.objects.filter(name=tag).first()  # Check if the tag already exists

                    if not tag_obj:
                        # Create a new tag if it doesn't exist
                        slug = slugify(tag, allow_unicode=True)
                        tag_obj = Tag.objects.create(name=tag, slug=slug)
                    
                    self.object.tags.add(tag_obj)  # Associate the tag with the post

            return response


def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()

                return redirect(comment.get_absolute_url())

        else:
            return redirect(post.get_absolute_url())
    
    else:
        raise PermissionDenied
    
class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    # Restrict post update to superusers, staff, or the author of the post
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied  # Raise permission denied if the user is not the author


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()        
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied
    
class PostSearch(PostList):
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs.get('q')
        post_list = Post.objects.filter(
            Q(title_contains=q) | Q(tags__name__contains=q)
        ).distinct()

        return post_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.kwargs.get('q')
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'

        return context