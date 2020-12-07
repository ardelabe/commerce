from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # path("listings", views.listings, name="listings"),
    path("sell", views.sell, name="sell"),
    path("<int:auction_id>", views.listings, name="listings"),
    path("watch", views.watch, name="watch"),
    path("comment", views.comment, name="comment")
]
