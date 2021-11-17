from django.contrib import admin
from .models import Genre, Actor, Content, User_like


admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Content)
admin.site.register(User_like)
