from django.shortcuts import render


from books.models import Library


def home(request):
	if request.user.is_authenticated:
		libraries = Library.objects.filter(user=request.user)
		return render(request, "base/home.html",{
			'libraries': libraries
		})
	else:	
		return render(request, "base/login.html")