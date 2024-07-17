from typing import Protocol

from rest_framework.response import Response


class ICommentRepo(Protocol):

    def create_comment(self, request, book_id: int) -> Response:
        ...


class IRatingRepo(Protocol):

    def create_rating(self, request, book_id: int) -> Response:
        ...

