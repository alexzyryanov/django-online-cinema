from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("movies/", views.movies, name="movies"),
    path("movies/<int:pk>/", views.movie, name="movie"),
    path("genres/", views.genres, name="genres"),
    path("genres/<int:pk>/", views.genre, name="genre"),
    path("actors/", views.actors, name="actors"),
    path("actors/<int:pk>/", views.actor, name="actor"),
    path("login/", views.user_login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.user_logout, name="logout"),
    path("api/", views.api, name="api"),
    path("account/", views.account, name="account")
]
