from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register),
    path("login", views.login),
    path("logout", views.logout),
    path("get_all_users", views.get_all_users),
    path("profile/<int:user_id>", views.get_user),
    path("profile/", views.profile),
    path("friend", views.friends),
    path("friends/<int:user_id>", views.make_friend)
]