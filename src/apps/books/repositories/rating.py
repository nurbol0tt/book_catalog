from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from src.apps.books.interfaces.persistence.repo import IRatingRepo
from apps.books.models import Book
from apps.books.serializers import RatingSerializer


class RatingRepo(IRatingRepo):

    def create_rating(self, request, book_id: int) -> Response:
        book = get_object_or_404(Book, id=book_id)
        serializer = RatingSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid()
        serializer.save(book=book)
        return Response(status=201)
