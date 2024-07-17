from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from src.apps.books.interfaces.persistence.repo import ICommentRepo
from apps.books.models import Book

from src.apps.books.serializers import CommentSerializer


class CommentRepo(ICommentRepo):

    def create_comment(self, request, book_id: int) -> Response:
        book = get_object_or_404(Book, id=book_id)
        serializer = CommentSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid()
        serializer.save(book=book)
        return Response(status=201)
