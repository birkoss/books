from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render, redirect, reverse

from .forms import BookForm, LibraryForm, LibraryCategoryForm
from .models import Book, Library, LibraryCategory


def library_single(request, library_slug):
	library = get_object_or_404(Library, slug=library_slug)
	
	return render(request, 'book/single.html', {
		'library': library
	})


@login_required
def edit_book(request, library_id, category_id, book_id):
	library = get_object_or_404(Library, pk=library_id)

	if library.user != request.user:
		return redirect('library/archive')

	category = get_object_or_404(LibraryCategory, pk=category_id)
	
	book = get_object_or_404(Book, pk=book_id)

	if request.method == "POST":
		form = BookForm(request.POST)

		if form.is_valid():
			book.name = form.cleaned_data['name']
			book.save()

			return redirect(reverse('library-category-book/edit', args=[library.id, category.id, book.id]) + "?status=updated")
	else:
		form = BookForm({
			'name': book.name
		})

	return render(request, 'book/book/edit.html', {
		'form': form,
		'library': library,
		'category': category,
	})


@login_required
def add_book(request, library_id, category_id):
	library = get_object_or_404(Library, pk=library_id)

	if library.user != request.user:
		return redirect('library/archive')

	category = get_object_or_404(LibraryCategory, pk=category_id)

	if request.method == "POST":
		form = BookForm(request.POST)

		if form.is_valid():
			book = Book(
				name = form.cleaned_data['name'], 
				category = category
			)
			book.save()

			return redirect(reverse('library-category-book/edit', args=[library.id, category.id, book.id]) + "?status=created")
	else:
		form = BookForm()

	return render(request, 'book/book/add.html', {
		'form': form,
		'library': library,
		'category': category,
	})


@login_required
def book_archive(request, library_id, category_id):
	library = get_object_or_404(Library, pk=library_id)

	if library.user != request.user:
		return redirect('library/archive')

	category = get_object_or_404(LibraryCategory, pk=category_id)

	return render(request, 'book/book/index.html', {
		'library': library,
		'category': category,
	})


@login_required
def edit_category(request, library_id, category_id):
	library = get_object_or_404(Library, pk=library_id)

	if library.user != request.user:
		return redirect('library/archive')

	category = get_object_or_404(LibraryCategory, pk=category_id)

	if request.method == "POST":
		form = LibraryCategoryForm(request.POST)

		if form.is_valid():
			category.name = form.cleaned_data['name']
			category.save()

			return redirect(reverse('library-category/edit', args=[library_id, category_id]) + "?status=updated")

	else:
		form = LibraryCategoryForm(initial={
			'name': category.name
		})

	return render(request, 'book/category/edit.html', {
		'form': form,
		'library': library
	})


@login_required
def add_category(request, library_id):
	library = get_object_or_404(Library, pk=library_id)

	if library.user != request.user:
		return redirect('library/archive')

	if request.method == "POST":
		form = LibraryCategoryForm(request.POST)

		if form.is_valid():
			category = LibraryCategory(
				name = form.cleaned_data['name'], 
				library = library
			)
			category.save()

			return redirect(reverse('library-category/edit', args=[library.id, category.id]) + "?status=created")
	else:
		form = LibraryCategoryForm()

	return render(request, 'book/category/add.html', {
		'form': form,
		'library': library,
	})


@login_required
def archive_category(request, library_id):
	library = get_object_or_404(Library, pk=library_id)

	if library.user != request.user:
		return redirect('library/archive')

	return render(request, 'book/category/index.html', {
		'library': library
	})



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