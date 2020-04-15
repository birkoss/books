from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render, redirect, reverse

from .forms import LibraryForm
from .models import Library


@login_required
def edit_library(request, library_id):
	library = get_object_or_404(Library, pk=library_id)

	if library.user != request.user:
		return redirect('library/archive')

	if request.method == "POST":
		form = LibraryForm(request.POST)

		if form.is_valid():
			library.name = form.cleaned_data['name']
			library.template = form.cleaned_data['template']
			library.save()

			return redirect(reverse('library/edit', args=[library_id]) + "?status=updated")

	else:
		form = LibraryForm(initial={
			'name': library.name,
			'template': library.template,
		})

	return render(request, 'book/edit.html', {
		'form': form
	})


@login_required
def add_library(request):
	if request.method == "POST":
		form = LibraryForm(request.POST)

		if form.is_valid():
			library = Library(
				name = form.cleaned_data['name'], 
				template = form.cleaned_data['template'], 
				user = request.user
			)
			library.save()

			return redirect(reverse('library/edit', args=[library.id]) + "?status=created")
	else:
		form = LibraryForm()

	return render(request, 'book/add.html', {
		'form': form
	})