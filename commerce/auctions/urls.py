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
    path("listing/create", views.create_listing, name="create_listing"),
    path("listing/<str:list_id>/edit", views.edit_listing, name="edit_listing"),
    path("listing/<str:list_id>/close", views.close_auction, name="close_auction"),
]
