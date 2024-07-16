from django.contrib import admin

from apps.books.models import Book, Genre, Comment, Note, Rating

# Register your models here.
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Comment)
admin.site.register(Note)
admin.site.register(Rating)
