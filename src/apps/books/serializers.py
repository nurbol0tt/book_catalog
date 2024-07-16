import django_filters
from django_filters import rest_framework as filters
from rest_framework import serializers

from apps.books.models import Comment, Rating, Book, Genre, Note
from apps.user.models import User


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ("text", "author")


class RatingSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Rating
        fields = ("star", "author")


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ("id", "title")


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username")


class BookListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    genres = GenreSerializer(many=True)
    average_rating = serializers.FloatField(read_only=True)
    in_notes = serializers.BooleanField(read_only=True)

    class Meta:
        model = Book
        fields = (
            "id", "title", "description",
            "publication_date", "genres", "author",
            "average_rating", "in_notes"
        )


class CommentListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "text", "author")


class BookDetailSerializer(BookListSerializer):
    comments = CommentListSerializer(
        source="comment_set", many=True, read_only=True
    )

    class Meta:
        model = Book
        fields = BookListSerializer.Meta.fields + ("comments",)


class NoteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Note
        fields = ("user",)


class ConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()


class BookFilter(filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="publication_date", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="publication_date", lookup_expr='lte')
    genres = django_filters.ModelMultipleChoiceFilter(queryset=Genre.objects.all())
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Book
        fields = ['genres', 'author', 'start_date', 'end_date']
