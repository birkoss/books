from django.shortcuts import render


def home(request):
	if request.user.is_authenticated:
		return render(request, "base/home.html")
	else:	
		return render(request, "base/login.html")