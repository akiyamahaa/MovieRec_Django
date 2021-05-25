from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.template import loader
from django.http import HttpResponse
from django.core.paginator import Paginator

from user.forms import SignupForm, ChangePasswordForm, EditProfileForm
from user.models import Profile
from movie.models import ReviewRating, Movie

# Create your views here.


def Signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			first_name = form.cleaned_data.get('first_name')
			last_name = form.cleaned_data.get('last_name')
			password = form.cleaned_data.get('password')
			User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
			return redirect('login')
	else:
		form = SignupForm()

	context = {
		'form': form,
	}

	return render(request, 'auth/signup.html', context)


@login_required
def ChangePassword(request):
	user = request.user
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			new_password = form.cleaned_data.get('new_password')
			user.set_password(new_password)
			user.save()
			update_session_auth_hash(request, user)
			return redirect('change-password-done')
	else:
		form = ChangePasswordForm(instance=user)

	context = {
		'form': form,
	}

	return render(request, 'auth/change_password.html', context)


def ChangePasswordDone(request):
	return render(request, 'auth/change_password_done.html')


@login_required
def EditProfile(request):
	user = request.user.id
	profile = Profile.objects.get(user__id=user)

	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES)
		if form.is_valid():
			profile.avatar = form.cleaned_data.get('avatar')
			profile.first_name = form.cleaned_data.get('first_name')
			profile.last_name = form.cleaned_data.get('last_name')
			profile.save()
			return redirect('home_page')
	else:
		form = EditProfileForm()

	context = {
		'form': form,
	}

	return render(request, 'edit_profile.html', context)

@login_required
def UserProfile(request,username):
	user = get_object_or_404(User,username=username)
	profile = Profile.objects.get(user=user)
	m_reviewed_count = ReviewRating.objects.filter(user=user).count()


	context ={
		'profile': profile,
		'm_reviewed_count': m_reviewed_count,
	}

	template = loader.get_template('profile.html')

	return HttpResponse(template.render(context,request))

@login_required
def UserListReviewed(request,username):
	user = get_object_or_404(User,username=username)
	profile = Profile.objects.get(user=user)

	m_reviewed_count = ReviewRating.objects.filter(user=user).count()
	movie_reviewed_list = []
	movies = ReviewRating.objects.filter(user=user)

	for movie in movies:
		if Movie.objects.filter(imdbID=movie.movie_id).exists():
			movie_data = Movie.objects.get(imdbID=movie.movie_id)
			movie_obj = {
				'Title': movie_data,
				'Poster': movie_data.Poster.url,
				'Year': movie_data.Year,
				'imdbID': movie.movie_id,
				'user_rated': movie.rate
			}
			movie_reviewed_list.append(movie_obj)
		else:
			url = 'http://www.omdbapi.com/?apikey=266c5967&i=' + movie.movie_id
			response = requests.get(url)
			movie_data = response.json()
			movie_data.user_rated = movie.rate
			movie_reviewed_list.append(movie_data)

	paginator = Paginator(movie_reviewed_list, 8)
	page_number = request.GET.get('page')
	movie_data = paginator.get_page(page_number)
	context ={
		'profile': profile,
		'm_reviewed_count': m_reviewed_count,
		'movie_data': movie_data,
		'list_title': 'Movie Reviewed',
	}

	template = loader.get_template('profile.html')

	return HttpResponse(template.render(context, request))

