from django.urls import path, include
from . import views


urlpatterns = [
    path("category/<str:slug>", views.category_page),   # 127.0.0.1/blog/cat
    path("<int:pk>", views.PostDetail.as_view()),   # 127.0.0.1/blog/1
    path("", views.PostList.as_view())              # 127.0.0.1/blog/
]
