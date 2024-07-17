from django.db.models import Avg, Exists, OuterRef
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from injector import inject
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.books.models import Book, Note
from apps.books.serializers import (
    CommentSerializer,
    RatingSerializer,
    BookListSerializer,
    BookDetailSerializer,
    NoteSerializer,
)

from src.apps.books.interfaces.persistence.reader import IBookReader
from src.apps.books.interfaces.persistence.repo import ICommentRepo, IRatingRepo
from src.apps.books.serializers import BookFilter


class CommentCreateView(APIView):
    """
    Only authorized can create a comment
    """
    permission_classes = [permissions.IsAuthenticated]

    @inject
    def __init__(self, service: ICommentRepo, *args, **kwargs):
        self.service = service

    @swagger_auto_schema(request_body=CommentSerializer)
    def post(self, request, book_id: int) -> Response:
        return self.service.create_comment(request, book_id)


class RatingCreateView(APIView):
    """
    Only authorized can create a comment
    """

    permission_classes = [permissions.IsAuthenticated]

    @inject
    def __init__(self, service: IRatingRepo, *args, **kwargs):
        self.service = service

    @swagger_auto_schema(request_body=CommentSerializer)
    def post(self, request, book_id: int) -> Response:
        return self.service.create_rating(request, book_id)


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

    @inject
    def __init__(self, service: IBookReader, *args, **kwargs):
        self.service = service

    def get(self, request, book_id: int) -> Response:
        return self.service.book_detail(request, book_id)


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