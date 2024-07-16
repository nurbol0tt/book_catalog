from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from apps.user.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True
    )
    email = models.EmailField(
        blank=True,
        null=True,
        unique=True,
    )
    is_staff = models.BooleanField(
        default=False,
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        auto_now=True
    )
    is_confirmed = models.BooleanField(
        default=False
    )

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self) -> str:
        return self.username
