from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from src.apps.books.models import Book
from src.apps.books.serializers import CommentSerializer, RatingSerializer


class CommentCreateView(APIView):
    """
    Only authorized can create a comment
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=CommentSerializer)
    def post(self, request, book_id: int) -> Response:
        book = get_object_or_404(Book, id=book_id)
        serializer = CommentSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid()
        serializer.save(book=book)
        return Response(status=201)


class RatingCreateView(APIView):
    """
    Only authorized can create a comment
    """

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=RatingSerializer)
    def post(self, request, book_id: int) -> Response:
        book = get_object_or_404(Book, id=book_id)
        serializer = RatingSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid()
        serializer.save(book=book)
        return Response(status=201)
