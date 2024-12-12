from django.contrib import admin

# Register your models here.

from .models import Reader, Book, Review

admin.site.register(Reader)
admin.site.register(Book)
admin.site.register(Review)