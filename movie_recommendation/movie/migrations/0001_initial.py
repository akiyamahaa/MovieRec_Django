# Generated by Django 3.2.2 on 2021-05-26 04:57

import django.contrib.auth.models
from django.db import migrations, models
import movie.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=50)),
                ('rating', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ReviewRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idx_user', models.CharField(blank=True, max_length=100, null=True)),
                ('idx_movie', models.CharField(blank=True, max_length=100, null=True)),
                ('rate', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')])),
                ('user', models.CharField(blank=True, max_length=100, null=True, verbose_name=django.contrib.auth.models.User)),
                ('movie_id', models.CharField(blank=True, max_length=100, null=True, verbose_name=movie.models.Movie)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=200)),
                ('Year', models.CharField(blank=True, max_length=25)),
                ('Rated', models.CharField(blank=True, max_length=10)),
                ('Released', models.CharField(blank=True, max_length=10)),
                ('Runtime', models.CharField(blank=True, max_length=25)),
                ('Director', models.CharField(blank=True, max_length=100)),
                ('Writer', models.CharField(blank=True, max_length=300)),
                ('Plot', models.CharField(blank=True, max_length=900)),
                ('Language', models.CharField(blank=True, max_length=300)),
                ('Country', models.CharField(blank=True, max_length=100)),
                ('Awards', models.CharField(blank=True, max_length=250)),
                ('Poster', models.ImageField(blank=True, upload_to='movies')),
                ('Poster_url', models.URLField(blank=True)),
                ('Metascore', models.CharField(blank=True, max_length=5)),
                ('imdbRating', models.CharField(blank=True, max_length=5)),
                ('imdbVotes', models.CharField(blank=True, max_length=100)),
                ('imdbID', models.CharField(blank=True, max_length=100)),
                ('Type', models.CharField(blank=True, max_length=10)),
                ('DVD', models.CharField(blank=True, max_length=25)),
                ('BoxOffice', models.CharField(blank=True, max_length=25)),
                ('Production', models.CharField(blank=True, max_length=100)),
                ('Website', models.CharField(blank=True, max_length=150)),
                ('totalSeasons', models.CharField(blank=True, max_length=3)),
                ('Actors', models.ManyToManyField(blank=True, to='movie.Actor')),
                ('Genre', models.ManyToManyField(blank=True, to='movie.Genre')),
                ('Ratings', models.ManyToManyField(blank=True, to='movie.Rating')),
            ],
        ),
        migrations.AddField(
            model_name='actor',
            name='movies',
            field=models.ManyToManyField(to='movie.Movie'),
        ),
    ]
