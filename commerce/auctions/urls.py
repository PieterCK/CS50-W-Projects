from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:specified_category>", views.category, name="category"),
    path("listing/<str:list_id>", views.listing, name="lists"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("edit_listing/<str:list_id>", views.edit_listing, name="edit_listing"),
]
