from django.contrib import admin
from movie.models import Movie,ReviewRating, Genre, Actor


# Register your models here.

admin.site.register(Movie)
admin.site.register(ReviewRating)
admin.site.register(Genre)
admin.site.register(Actor)


