from django.db import models
from django.contrib.auth.models import User
# from blog.models import Post as ps
import os


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/news/category/{self.slug}'

    class Meta:
        verbose_name_plural = 'Categories'

# Create your models here.
class NewsPost(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    name = models.CharField(max_length=10)
    hook_text = models.CharField(max_length=100, blank=True)

    email = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    head_image = models.ImageField(upload_to='images/%Y/%m/%d/', blank=True)
    # author = ps.author
    # category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)

    author_news = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category_news = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'[{self.pk - 1}]{self.title} :: {self.author}'
    
    def get_absolute_url(self):
        return f'/news/{self.pk}'
    
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)
    
    def get_file_ext(self):
        return self.get_file_name().rsplit('.', maxsplit=1)[-1]