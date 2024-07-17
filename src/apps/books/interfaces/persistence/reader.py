from asyncio import Protocol

from rest_framework.response import Response


class IBookReader(Protocol):

    def book_list(self):
        ...

    def book_detail(self, request, book_id) -> Response:
        ...
