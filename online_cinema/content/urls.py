from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("movies/", views.movies, name="movies"),
    path("movies/<int:pk>/", views.film, name="film"),
    path("genres/", views.genres, name="genres"),
    path("genres/<int:pk>/", views.genre_films, name="genre_films"),
    path("actors/", views.actors, name="actors"),
    path("actors/<int:pk>/", views.actor_about, name="actor_about"),
    path("login/", views.user_login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.user_logout, name="logout"),
    path("api/", views.api, name="api"),
    path("account/", views.account, name="account")
]
