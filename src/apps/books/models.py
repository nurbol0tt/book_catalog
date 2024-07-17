from django.db import models

from apps.user.models import User


class Genre(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    publication_date = models.DateField()
    genres = models.ManyToManyField(
        Genre
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


class Note(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, related_name='notes')


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

