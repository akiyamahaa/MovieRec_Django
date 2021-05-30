from django.urls import path
from movie.views import home_page,pagination, movie_details,Rate, search_by_genres, search_by_actors,addMoviesToWatch

urlpatterns = [
  path('search/<query>/page/<page_number>',pagination,name='pagination'),
  path('<imdb_id>',movie_details,name='movie-details'),
  path('<imdb_id>/rate',Rate,name='rate-movie'),
  path('genre/<slug:genre_slug>', search_by_genres, name='genres'),
  path('actor/<slug:actor_slug>', search_by_actors, name='actors'),
	path('<imdb_id>/addtomoviewatch', addMoviesToWatch, name='add-movies-to-watch'),

]