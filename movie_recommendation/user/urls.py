from django.urls import path

from user.views import Signup, ChangePassword, ChangePasswordDone, EditProfile
from django.contrib.auth import views as authViews

urlpatterns =[
	path('profile/edit', EditProfile, name='edit-profile'),
	path('signup/', Signup, name='signup'),
	path('login/', authViews.LoginView.as_view(template_name='auth/login.html'), name='login'),
	path('logout/', authViews.LogoutView.as_view(), {'next_page': 'login'}, name='logout'),
	path('changepassword/', ChangePassword, name='change-password'),
	path('changepassword/done', ChangePasswordDone, name='change-password-done'),
	path('passwordreset/', authViews.PasswordResetView.as_view(), name='password_reset_form'),
	path('passwordreset/done', authViews.PasswordResetDoneView.as_view(), name='password_reset_done'),
	path('passwordreset/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	path('passwordreset/complete', authViews.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]