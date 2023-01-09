from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entryPage, name="entries"),
    path("new_entry", views.newEntry, name="new_entry"),
    path("edit_entry/<str:title>", views.editEntry, name="edit_entry"),
    path("rand_entry", views.randomEntry, name="rand_entry"),
]
