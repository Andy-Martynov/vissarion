from django.contrib import admin

from .models import Author, Writing, Sample

admin.site.register(Author)
admin.site.register(Writing)
admin.site.register(Sample)

