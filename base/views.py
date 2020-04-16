from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from books.models import Library


@login_required
def logout_user(request):
	logout(request)
	return redirect('home')


def home(request):
	if request.user.is_authenticated:
		libraries = Library.objects.filter(user=request.user)
		return render(request, "base/home.html",{
			'libraries': libraries
		})
	else:	
		return render(request, "base/login.html")