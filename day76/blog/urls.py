from django.urls import path, include
from . import views


urlpatterns = [
    path("update_post/<int:pk>", views.PostUpdate.as_view()),   # 127.0.0.1/blog/create_post/
    path("create_post/", views.PostCreate.as_view()),   # 127.0.0.1/blog/create_post/
    path("tag/<str:slug>", views.tag_page),   # 127.0.0.1/blog/tag/경제
    path("category/<str:slug>", views.category_page),   # 127.0.0.1/blog/category/경제
    path("<int:pk>", views.PostDetail.as_view()),   # 127.0.0.1/blog/1
    path("", views.PostList.as_view())              # 127.0.0.1/blog/
]
