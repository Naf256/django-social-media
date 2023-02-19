
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("page/<int:page_num>", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="post"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("profile/<int:id>/page/<int:page_num>", views.profile, name="profile"),
    path("follow/<int:id>", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("following/page/<int:page_num>", views.following, name="following"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("like/<int:id>/", views.like, name="like")
]
