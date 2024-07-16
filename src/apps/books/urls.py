from django.urls import path

from apps.books.views.views import CommentCreateView, RatingCreateView, BookListView, BookDetailView, NoteCreateView

urlpatterns = [
    path("comment/<int:book_id>/", CommentCreateView.as_view()),
    path("rating/<int:book_id>/", RatingCreateView.as_view()),

    path("book/list/", BookListView.as_view()),
    path("book/<int:book_id>/", BookDetailView.as_view()),
    path("book/<int:book_id>/save/", NoteCreateView.as_view()),
]
