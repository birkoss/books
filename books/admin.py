from django.contrib import admin

from .models import Library, LibraryCategory, LibraryTemplate, Book


admin.site.register(Library)
admin.site.register(LibraryCategory)
admin.site.register(Book)
admin.site.register(LibraryTemplate)