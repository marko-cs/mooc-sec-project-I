""" URL patter routing to views """

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("add_new/", views.addnew_view, name="add_new"),
    path("delete/<uuid:item_id>", views.delete_view, name="delete"),
]
