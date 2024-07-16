from django.db.models import Avg, Exists, OuterRef
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.books.models import Book, Note
from apps.books.serializers import (
    CommentSerializer,
    RatingSerializer,
    BookListSerializer,
    BookDetailSerializer, NoteSerializer,
)

from src.apps.books.serializers import BookFilter


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


class BookListView(ListAPIView):
    queryset = Book.objects.all().annotate(average_rating=Avg('rating__star'))
    serializer_class = BookListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            in_notes=Exists(
                Note.objects.filter(
                    user=self.request.user, books=OuterRef('pk')
                )
            )
        ).select_related('author').prefetch_related('genres')
        return queryset


class BookDetailView(APIView):

    def get(self, request, book_id) -> Response:
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


class NoteCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, book_id) -> Response:
        book = get_object_or_404(Book, id=book_id)
        notes = Note.objects.filter(user=request.user)

        if notes.exists():
            note = notes.first()
            note.books.add(book)
            serializer = NoteSerializer(instance=note)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = NoteSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid()
        notes = serializer.save(books=[book])
        notes.books.add(book)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
