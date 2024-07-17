from injector import Module, singleton

from src.apps.books.interfaces.persistence.reader import IBookReader
from src.apps.books.interfaces.persistence.repo import ICommentRepo, IRatingRepo
from src.apps.books.repositories.book import BookReader
from src.apps.books.repositories.comment import CommentRepo
from src.apps.books.repositories.rating import RatingRepo


class MyModule(Module):
    def configure(self, binder):
        binder.bind(ICommentRepo, to=CommentRepo, scope=singleton)
        binder.bind(IRatingRepo, to=RatingRepo, scope=singleton)
        binder.bind(IBookReader, to=BookReader, scope=singleton)
