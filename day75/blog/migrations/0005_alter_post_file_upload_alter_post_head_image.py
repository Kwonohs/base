# Generated by Django 5.1.3 on 2024-11-25 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_file_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='file_upload',
            field=models.FileField(blank=True, upload_to='files/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='head_image',
            field=models.ImageField(blank=True, upload_to='images/%Y/%m/%d/'),
        ),
    ]
