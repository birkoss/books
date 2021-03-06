from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from social_django.models import UserSocialAuth

from books.models import Library


@login_required
def user_logout(request):
	logout(request)
	return redirect('home')


@login_required
def user_profile(request):
	user = request.user

	try:
		github_login = user.social_auth.get(provider='github')
	except UserSocialAuth.DoesNotExist:
		github_login = None

	try:
		google_login = user.social_auth.get(provider='google-oauth2')
	except UserSocialAuth.DoesNotExist:
		google_login = None

	try:
		facebook_login = user.social_auth.get(provider='facebook')
	except UserSocialAuth.DoesNotExist:
		facebook_login = None

	can_disconnect = (user.social_auth.count() > 1)

	return render(request, 'base/profile.html', {
		'github_login': github_login,
		'google_login': google_login,
		'facebook_login': facebook_login,
		'can_disconnect': can_disconnect
	})


def home(request):
	if request.user.is_authenticated:
		libraries = Library.objects.filter(user=request.user)
		return render(request, "base/home.html",{
			'libraries': libraries
		})
	else:	
		return render(request, "base/login.html")