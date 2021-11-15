from django.db import models


class Genre(models.Model):
    name_genre = models.CharField(max_length=200, verbose_name="Название жанра")

    def __str__(self):
        return self.name_genre
    
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Actor(models.Model):
    name_actor = models.CharField(max_length=200, verbose_name="Имя актера")
    about_actor = models.TextField(verbose_name="Инфо об актере")
    image_actor = models.URLField(verbose_name="Ссылка на фото")

    def __str__(self):
        return self.name_actor
    
    class Meta:
        verbose_name = "Актер"
        verbose_name_plural = "Актеры"


class Content(models.Model):
    name_film = models.CharField(max_length=200, verbose_name="Название фильма")
    cover_film = models.URLField(verbose_name="Ссылка на обложку")
    video_film = models.URLField(verbose_name="Ссылка на видео")
    about_film = models.TextField(verbose_name="Инфо о фильме")
    id_film = models.CharField(max_length=200, verbose_name="id фильма")
    actors = models.ManyToManyField(Actor, verbose_name="Актеры из фильма")
    genres = models.ManyToManyField(Genre, verbose_name="Жанры фильма")
    years = models.BigIntegerField(verbose_name="Год выхода")


    def __str__(self):
        return self.name_film
    
    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
