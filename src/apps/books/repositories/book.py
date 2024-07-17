from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from src.apps.books.interfaces.persistence.reader import IBookReader
from apps.books.models import Book
from apps.books.serializers import BookDetailSerializer


class BookReader(IBookReader):

    def book_list(self):
        ...

    def book_detail(self, request, book_id):
        book = get_object_or_404(
            Book.objects.annotate(
                average_rating=Avg('rating__star')
            )
            .select_related('author')
            .prefetch_related('genres', 'comment_set__author'),
            id=book_id,
        )
        serializer = BookDetailSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
