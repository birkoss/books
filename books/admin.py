from django.contrib import admin

from .models import Library, LibraryTemplate


admin.site.register(Library)
admin.site.register(LibraryTemplate)