from django.contrib import admin
from django.urls import path


from books import views as books_views
from base import views as base_views

urlpatterns = [
    path('', base_views.home, name='library/archive'),
    path('libraries/add', books_views.add_library, name='library/add'),
    path('libraries/edit/<str:library_id>', books_views.edit_library, name='library/edit'),
    path('admin/', admin.site.urls),
]
