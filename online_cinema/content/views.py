from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Content, Genre, Actor


def index(request):
    movies = Content.objects.all()[:10]
    genres = Genre.objects.all()
    actors = Actor.objects.all()[:14]
    return render(request, 'content/index.html', {'movies': movies, 'genres': genres, 'actors': actors})


def movies(request):
    movies = Content.objects.all()
    paginator = Paginator(movies, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'content/movies.html', {'page_obj': page_obj})


def film(request, pk):
    movies = Content.objects.filter(id=pk)
    actors = Content.objects.get(id=pk).actors.all()
    genres = Content.objects.get(id=pk).genres.all()
    return render(request, 'content/film.html', {'movies': movies, 'actors': actors, 'genres': genres})


def genres(request):
    genres = Genre.objects.all()
    return render(request, 'content/genres.html', {'genres': genres})


def genre_films(request, pk):
    movies = Content.objects.filter(genres__id=pk)
    return render(request, 'content/genre_films.html', {'movies': movies})


def actors(request):
    actors = Actor.objects.all()
    paginator = Paginator(actors, 14)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'content/actors.html', {'page_obj': page_obj})


def actor_about(request, pk):
    actor = Actor.objects.filter(id=pk)
    movies = Content.objects.filter(actors__id=pk)
    return render(request, 'content/actor_about.html', {'actor': actor, 'movies': movies})
