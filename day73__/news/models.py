from django.db import models

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
        return f'[{self.pk}]{self.title}'