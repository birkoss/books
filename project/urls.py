from django.contrib import admin
from django.urls import path


from books import views as books_views
from base import views as base_views

urlpatterns = [
    path('', base_views.home, name='library/archive'),
    path('library/<str:library_slug>/', books_views.library_single, name='library/single'),
    path('libraries/add/', books_views.add_library, name='library/add'),
    path('libraries/edit/<str:library_id>/categories/edit/<str:category_id>/books/edit/<str:book_id>/', books_views.edit_book, name='library-category-book/edit'),
    path('libraries/edit/<str:library_id>/categories/edit/<str:category_id>/books/add/', books_views.add_book, name='library-category-book/add'),
    path('libraries/edit/<str:library_id>/categories/edit/<str:category_id>/books/', books_views.book_archive, name='library-category-book/archive'),
    path('libraries/edit/<str:library_id>/categories/edit/<str:category_id>/', books_views.edit_category, name='library-category/edit'),
    path('libraries/edit/<str:library_id>/categories/add/', books_views.add_category, name='library-category/add'),
    path('libraries/edit/<str:library_id>/categories/', books_views.archive_category, name='library-category/archive'),
    path('libraries/edit/<str:library_id>/', books_views.edit_library, name='library/edit'),
    path('admin/', admin.site.urls),
]
