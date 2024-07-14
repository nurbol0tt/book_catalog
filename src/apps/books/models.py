from django.db import models

from src.apps.user.models import User


class Genre(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    publication_date = models.DateField()
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        "Messages",
        max_length=5000
    )
    parent = models.ForeignKey(
        'self',
        verbose_name="Parent",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="children"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.username} - {self.book}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.book.title}'


class Rating(models.Model):
    star = models.FloatField(default=0)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

