from requests.api import request
import csv
import io
import numpy as np
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.utils.text import slugify
from django.urls import reverse
from django.db.models import Count
from django.conf import settings
from django.core.paginator import Paginator

import tensorflow as tf

from movie.models import ReviewRating
from movie.models import Movie, Genre, Rating, Actor
from movie.forms import RateForm
from user.models import Profile

import requests
import random

# Create your views here.
from django.contrib.auth.decorators import login_required


def get_popular_movie_id():
    top_movie_path = settings.DATA_ROOT + "/top_movie.csv"
    top_movie_id = []
    with open(top_movie_path) as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            top_movie_id.append(row[0])

    return random.choices(top_movie_id, k=10)


def home_page(request):
    query = request.GET.get("q")
    if query:
        url = "http://www.omdbapi.com/?apikey=266c5967&s=" + query
        response = requests.get(url)
        movie_data = response.json()

        context = {"query": query, "movie_data": movie_data, "page_number": 1}

        template = loader.get_template("search_results.html")
        return HttpResponse(template.render(context, request))

    top_movie_data = []
    top_movie_arr = get_popular_movie_id()
    for movie_id in top_movie_arr:
        # if Movie.objects.filter(imdbID=movie_id).exists():
        #     movie_data = Movie.objects.get(imdbID=movie_id)
        #     movie_obj = {
        #         "Title": movie_data.Title,
        #         "Poster": movie_data.Poster.url,
        #         "Year": movie_data.Year,
        #     }
        #     top_movie_data.append(movie_obj)
        # else:
        url = "http://www.omdbapi.com/?apikey=266c5967&i=" + movie_id
        response = requests.get(url)
        movie_data = response.json()
        top_movie_data.append(movie_data)

    template = loader.get_template("homepage.html")

    context = {"movie_data": top_movie_data}

    return HttpResponse(template.render(context, request))


def pagination(request, query, page_number):
    page_number = int(page_number) + 1
    url = (
        "http://www.omdbapi.com/?apikey=266c5967&s="
        + query
        + "&page="
        + str(page_number)
    )
    response = requests.get(url)
    movie_data = response.json()
    context = {
        "query": query,
        "movie_data": movie_data,
        "page_number": page_number,
    }

    template = loader.get_template("search_results.html")

    return HttpResponse(template.render(context, request))


def movie_details(request, imdb_id):
    if Movie.objects.filter(imdbID=imdb_id).exists():
        movie_data = Movie.objects.get(imdbID=imdb_id)
        exists_db = True

        context = {
            "movie_data": movie_data,
            "exists_db": exists_db,
        }

    else:
        url = "http://www.omdbapi.com/?apikey=266c5967&i=" + imdb_id
        response = requests.get(url)
        movie_data = response.json()

        rating_objs = []
        genre_objs = []
        actor_objs = []

        # For actor
        actor_list = [x.strip() for x in movie_data["Actors"].split(",")]
        for actor in actor_list:
            each_actor, created = Actor.objects.get_or_create(name=actor)
            actor_objs.append(each_actor)

        # For genre
        genre_list = list(movie_data["Genre"].replace(" ", "").split(","))
        for genre in genre_list:
            genre_slug = slugify(genre)
            each_genre, created = Genre.objects.get_or_create(
                title=genre, slug=genre_slug
            )
            genre_objs.append(each_genre)

        # For Rating
        for rate in movie_data["Ratings"]:
            each_rate, created = Rating.objects.get_or_create(
                source=rate["Source"], rating=rate["Value"]
            )
            rating_objs.append(each_rate)

        if movie_data["Type"] == "movie":
            each_movie, created = Movie.objects.get_or_create(
                Title=movie_data["Title"],
                Year=movie_data["Year"],
                Rated=movie_data["Rated"],
                Released=movie_data["Released"],
                Runtime=movie_data["Runtime"],
                Director=movie_data["Director"],
                Writer=movie_data["Writer"],
                Plot=movie_data["Plot"],
                Language=movie_data["Language"],
                Country=movie_data["Country"],
                Awards=movie_data["Awards"],
                Poster_url=movie_data["Poster"],
                Metascore=movie_data["Metascore"],
                imdbRating=movie_data["imdbRating"],
                imdbVotes=movie_data["imdbVotes"],
                imdbID=movie_data["imdbID"],
                Type=movie_data["Type"],
                DVD=movie_data["DVD"],
                BoxOffice=movie_data["BoxOffice"],
                Production=movie_data["Production"],
                Website=movie_data["Website"],
            )
            each_movie.Genre.set(genre_objs)
            each_movie.Actors.set(actor_objs)
            each_movie.Ratings.set(rating_objs)

        else:
            # For the series movie
            each_movie, created = Movie.objects.get_or_create(
                Title=movie_data["Title"],
                Year=movie_data["Year"],
                Rated=movie_data["Rated"],
                Released=movie_data["Released"],
                Runtime=movie_data["Runtime"],
                Director=movie_data["Director"],
                Writer=movie_data["Writer"],
                Plot=movie_data["Plot"],
                Language=movie_data["Language"],
                Country=movie_data["Country"],
                Awards=movie_data["Awards"],
                Poster_url=movie_data["Poster"],
                Metascore=movie_data["Metascore"],
                imdbRating=movie_data["imdbRating"],
                imdbVotes=movie_data["imdbVotes"],
                imdbID=movie_data["imdbID"],
                Type=movie_data["Type"],
                totalSeasons=movie_data["totalSeasons"],
            )
            each_movie.Genre.set(genre_objs)
            each_movie.Actors.set(actor_objs)
            each_movie.Ratings.set(rating_objs)

        each_movie.save()
        exists_db = False

        context = {
            "movie_data": movie_data,
            "exists_db": exists_db,
        }

    template = loader.get_template("movie_details.html")

    return HttpResponse(template.render(context, request))


def search_by_genres(request, genre_slug):
    genre = get_object_or_404(Genre, slug=genre_slug)
    movies = Movie.objects.filter(Genre=genre)

    paginator = Paginator(movies, 9)
    page_number = request.GET.get('page')
    movie_data = paginator.get_page(page_number)

    context = {
        'movie_data': movie_data,
        'genre': genre,
    }

    template = loader.get_template('genre.html')

    return HttpResponse(template.render(context, request))


def search_by_actors(request, actor_slug):
    actor = get_object_or_404(Actor, slug=actor_slug)
    movies = Movie.objects.filter(Actors=actor)

    paginator = Paginator(movies, 9)
    page_number = request.GET.get('page')
    movie_data = paginator.get_page(page_number)

    context = {
        'movie_data': movie_data,
        'actor': actor,
    }

    template = loader.get_template('actor.html')

    return HttpResponse(template.render(context, request))


@login_required(login_url="/account/login")
def Rate(request, imdb_id):
    movie = Movie.objects.get(imdbID=imdb_id)
    user = request.user
    profile = Profile.objects.get(user=user)
    user_exist = ReviewRating.objects.filter(user=user)
    movie_exist = ReviewRating.objects.filter(movie_id=imdb_id)
    # Remove movie from watch-list
    if profile.to_watch.filter(imdbID=imdb_id).exists():
        profile.to_watch.remove(movie)      

    user_count = len(
        ReviewRating.objects.values("idx_user").annotate(
            Count("idx_user", distinct=True)
        )
    )
    movie_count = len(
        ReviewRating.objects.values("idx_movie").annotate(
            Count("idx_movie", distinct=True)
        )
    )

    if request.method == "POST":
        # Delete User rating exist
        if len(user_exist) > 0 and len(movie_exist) > 0:
            ReviewRating.objects.filter(user=user, movie_id=imdb_id).delete()
        form = RateForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            if len(user_exist):
                rate.idx_user = user_exist[0].idx_user
            else:
                rate.idx_user = int(user_count)
            if len(movie_exist):
                rate.idx_movie = movie_exist[0].idx_movie
            else:
                rate.idx_movie = int(movie_count)
            rate.user = user
            rate.movie_id = imdb_id

            rate.save()
            return HttpResponseRedirect(reverse("movie-details", args=[imdb_id]))
    else:
        form = RateForm()

    template = loader.get_template("rate.html")

    context = {
        "form": form,
        "movie": movie,
    }

    return HttpResponse(template.render(context, request))


def addMoviesToWatch(request, imdb_id):
    movie = Movie.objects.get(imdbID=imdb_id)
    user = request.user
    profile = Profile.objects.get(user=user)

    profile.to_watch.add(movie)

    return HttpResponseRedirect(reverse('movie-details', args=[imdb_id]))

def rating_upload(request):
    template = loader.get_template("rating_upload.html")
    prompt = {"order": "order of the CSV is idx_user,idx_movie,rating,user,movie_id"}

    if request.method == "GET":
        return HttpResponse(template.render(prompt, request))

    csv_file = request.FILES["file"]

    if not csv_file.name.endswith(".csv"):
        messages.error(request, "This is not csv file")

    data_set = csv_file.read().decode("UTF_8")
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=","):
        ReviewRating.objects.bulk_create(
            [
                ReviewRating(
                    idx_user=column[0],
                    idx_movie=column[1],
                    rate=column[2],
                    user=column[3],
                    movie_id=column[4],
                )
            ]
        )
    context = {}
    return HttpResponse(template.render(context, request))

# RECOMMENDATION
def get_raw_mid(mid):
    return ReviewRating.objects.filter(idx_movie=mid)[0].movie_id

def get_movie_rec_id_and_pred(predictions,k=10):
    recommended_book_ids = (-predictions).argsort()[:k]
    dict_raw_mid = {}
    for mid in recommended_book_ids:
        dict_raw_mid[get_raw_mid(mid)] = predictions[mid]
    return dict_raw_mid

@login_required(login_url="/account/login")
def get_my_recommendation(request):
    model_path = settings.MODEL_ROOT + "/MF_keras.h5"
    model_keras = tf.keras.models.load_model(model_path)
    user = request.user
    idx_user = int(ReviewRating.objects.filter(user=user)[0].idx_user)

    glob_mean = 6.935751112458413

    top_movie_data = []
    
    total_mid = ReviewRating.objects.values_list(
        'idx_movie', flat=True).distinct()
    total_mid = np.array(total_mid)
    mid_predicted = ReviewRating.objects.filter(
        user=user).values_list('idx_movie', flat=True).distinct()
    mid_predicted = np.array(mid_predicted)
    mid_not_predicted = total_mid.copy()
    for i in mid_predicted:
        mid_not_predicted = np.delete(
            mid_not_predicted, np.where(mid_not_predicted == i))
    mid_not_predicted = mid_not_predicted.astype(int)
    usr_arr = np.array([idx_user for i in range(len(mid_not_predicted))])
    predictions = model_keras.predict([usr_arr, mid_not_predicted])
    predictions += glob_mean
    predictions = np.array([a[0] for a in predictions])
    my_recommendation = get_movie_rec_id_and_pred(predictions)
    
    for movie_id,predict_score in my_recommendation.items():
        if Movie.objects.filter(imdbID=movie_id).exists():
            movie_data = Movie.objects.get(imdbID=movie_id)
            movie_obj = {
                'Title': movie_data.Title,
                'Poster': movie_data.Poster.url,
                'Year': movie_data.Year,
                'predict_score':predict_score 
            }
            top_movie_data.append(movie_obj)
        else:
            url = 'http://www.omdbapi.com/?apikey=266c5967&i=' + movie_id
            response = requests.get(url)
            movie_data = response.json()
            movie_data['predict_score'] = predict_score
            top_movie_data.append(movie_data)
            

    template = loader.get_template("my_recommendation.html")

    context = {"movie_data": top_movie_data}

    return HttpResponse(template.render(context, request))
