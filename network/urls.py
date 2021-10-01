
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:profileid>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("like_post", views.like, name="like"),
    path("unlike_post", views.unlike, name="unlike"),
    path("edit_post", views.edit, name="edit")
]
