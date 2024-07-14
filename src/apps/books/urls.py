from django.urls import path

from src.apps.books.views.views import CommentCreateView, RatingCreateView

urlpatterns = [
    path("comment/<int:book_id>/", CommentCreateView.as_view()),
    path("rating/<int:book_id>/", RatingCreateView.as_view()),
    path("book/list", RatingCreateView.as_view()),
    path("book/<int:id>/", RatingCreateView.as_view()),
    path("book/save/", RatingCreateView.as_view()),
]