from django.db import models
import os

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    name = models.CharField(max_length=10)
    hook_text = models.CharField(max_length=100, blank=True)

    email = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    head_image = models.ImageField(upload_to='images/%Y/%m/%d/', blank=True)


    def __str__(self):
        return f'[{self.pk - 1}]{self.title}'
    
    def get_absolute_url(self):
        return f'/news/{self.pk}'
    
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)
    
    def get_file_ext(self):
        return self.get_file_name().rsplit('.', maxsplit=1)[-1]