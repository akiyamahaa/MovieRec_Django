from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.template import loader
from django.http import HttpResponse

from user.forms import SignupForm, ChangePasswordForm, EditProfileForm
from user.models import Profile

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
			profile.profile_info = form.cleaned_data.get('profile_info')
			profile.save()
			return redirect('index')
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

	context ={
		'profile': profile
	}

	template = loader.get_template('profile.html')

	return HttpResponse(template.render(context,request))