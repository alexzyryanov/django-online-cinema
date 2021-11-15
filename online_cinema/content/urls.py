from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('movies/', views.movies, name='movies'),
    path('movies/<int:pk>/', views.film, name='film'),
    path('genres/', views.genres, name='genres'),
    path('genres/<int:pk>/', views.genre_films, name='genre_films'),
    path('actors/', views.actors, name='actors'),
    path('actors/<int:pk>/', views.actor_about, name='actor_about')
]
