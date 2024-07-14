from django.contrib import admin

from src.apps.books.models import Book, Genre, Comment, Favorite, Rating

# Register your models here.
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Comment)
admin.site.register(Favorite)
admin.site.register(Rating)
