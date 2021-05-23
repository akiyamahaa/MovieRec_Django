from django.contrib import admin
from movie.models import Movie, Review,ReviewRating


# Register your models here.


admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(ReviewRating)


