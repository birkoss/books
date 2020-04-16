import os
import os.path
import shutil

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.utils.text import slugify

from imagekit.utils import get_cache

from project.config import MEDIA_ROOT, MEDIA_URL
from project.utils import get_existing_image

from .forms import BookForm, LibraryForm, LibraryCategoryForm
from .models import Book, Library, LibraryCategory


def library_single(request, library_slug):
	library = get_object_or_404(Library, slug=library_slug)

	categories = []

	# @TODO Verify that this library is active

	for single_category in library.librarycategory_set.all():
		category = {
			'name': single_category.name,
			'books': []
		}
		for single_book in single_category.book_set.all():
			cover_image = get_existing_image(single_book.cover)

			if cover_image:
				category['books'].append({
					'name': single_book.name,
					'url': single_book.url,
					'cover_image': cover_image
				})

		if category['books']:
			categories.append(category)
	
	return render(request, 'book/single.html', {
		'library': library,
		'categories': categories
	})


@login_required
# @TODO : Combine edit and add
# @TODO : Validate url starting with http.
# @TODO : Allow NO url for quick save
# @TODO : BTN Save and Stay, Save and Back
def edit_book(request, library_id, category_id, book_id):
	library = get_object_or_404(Library, pk=library_id)

	if library.user != request.user:
		return redirect('library/archive')

	category = get_object_or_404(LibraryCategory, pk=category_id)
	
	book = get_object_or_404(Book, pk=book_id)

	book_cover_image = get_existing_image(book.cover)

	if request.method == "POST":
		form = BookForm(request.POST)

		if form.is_valid():
			# Check if there are posted images.
			if request.FILES.getlist('cover'):

				# If a cover image is already there ?
				if book.cover:
					# Delete the imagekit CACHE folder
					(image_folder, image_extension) = os.path.splitext(book.cover.url)
					image_folder = MEDIA_ROOT + "/CACHE/images/" + image_folder.replace(MEDIA_URL, "")
					try:
						shutil.rmtree(image_folder)
					except FileNotFoundError:
						pass

					# Delete the book cover
					book.cover.delete()

				# Save the new Book cover
				book_medias_path = 'books/' + str(book.id)
				for post_file in request.FILES.getlist('cover'):
					(image_filename, image_extension) = os.path.splitext(post_file.name)

					fs = FileSystemStorage(location=MEDIA_ROOT + "/" + book_medias_path)
					filename = fs.save(slugify(image_filename)+image_extension, post_file)

					book.cover = book_medias_path + '/' + filename

			book.name = form.cleaned_data['name']
			book.url = form.cleaned_data['url']
			book.save()

			return redirect(reverse('library-category-book/edit', args=[library.id, category.id, book.id]) + "?status=updated")
	else:
		form = BookForm({
			'name': book.name,
			'url': book.url,
		})

	return render(request, 'book/book/edit.html', {
		'form': form,
		'library': library,
		'category': category,
		'book': book,
		'book_cover_image': book_cover_image
	})


@login_required
# @TODO : Allow image upload in the ADD
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
				url = form.cleaned_data['url'], 
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
def edit_library(request, library_id=None):
	library = None

	if library_id:
		library = get_object_or_404(Library, pk=library_id)

		if library.user != request.user:
			return redirect('library/archive')

	if request.method == "POST":
		form = LibraryForm(request.POST)

		if form.is_valid():
			if library_id is None:
				library = Library(user = request.user)

			library.name = form.cleaned_data['name']
			library.template = form.cleaned_data['template']
			library.save()

			return redirect(reverse('library/edit', args=[library.id]) + "?status=" + ("updated" if library_id else "created"))

	elif library_id:
		form = LibraryForm(initial={
			'name': library.name,
			'template': library.template,
		})
	else:
		form = LibraryForm()

	return render(request, 'book/library/edit.html', {
		'form': form,
		'button': ('Modifier' if library_id else 'Ajouter'),
		'title': ('Modifier une bibliothèque existante' if library_id else 'Ajouter une nouvelle bibliothèque'),
	})
