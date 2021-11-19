from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponse, redirect
from .models import Content, Genre, Actor, User_like

from .forms import UserRegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
import json


def index(request):
    movies = Content.objects.all()[:10]
    genres = Genre.objects.all()
    actors = Actor.objects.all()[:14]
    return render(request, "content/index.html", {"movies": movies, "genres": genres, "actors": actors})


def movies(request):
    movies = Content.objects.all()
    paginator = Paginator(movies, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "content/movies.html", {"page_obj": page_obj})


def film(request, pk):
    movies = Content.objects.filter(id = pk)
    actors = Content.objects.get(id = pk).actors.all()
    genres = Content.objects.get(id = pk).genres.all()
    return render(request, "content/film.html", {"movies": movies, "actors": actors, "genres": genres})


def genres(request):
    genres = Genre.objects.all()
    return render(request, "content/genres.html", {"genres": genres})


def genre_films(request, pk):
    movies = Content.objects.filter(genres__id = pk)
    return render(request, "content/genre_films.html", {"movies": movies})


def actors(request):
    actors = Actor.objects.all()
    paginator = Paginator(actors, 14)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "content/actors.html", {"page_obj": page_obj})


def actor_about(request, pk):
    actor = Actor.objects.filter(id = pk)
    movies = Content.objects.filter(actors__id = pk)
    return render(request, "content/actor_about.html", {"actor": actor, "movies": movies})


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit = False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            user_like = User_like(user = request.POST["username"])
            user_like.save()
            user = authenticate(username = request.POST["username"], password = user_form.cleaned_data["password"])
            login(request, user)
            return redirect("/")
    else:
        user_form = UserRegistrationForm()
    return render(request, "content/register.html", {"user_form": user_form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("/")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, "content/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("/")


def api(request):
    if str(request.user) != "AnonymousUser":
        data = json.loads(request.body)
        if data["type"] == "like":
            user_like = User_like.objects.get(user = request.user)
            user_like.like.add(data["id"])
            return HttpResponse("like append")
        elif data["type"] == "like_del":
            user_like_del = User_like.objects.get(user = request.user)
            user_like_del.like.remove(data["id"])
            return HttpResponse("like del")
    else:
        return HttpResponse("need register")


def account(request):
    movies = User_like.objects.get(user = request.user).like.all()
    return render(request, "content/account.html", {"movies": movies})
