from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def _create(self, email,  password, **extra):
        """
        Creates and saves a User with the given username and password.
        """
        if not email:
            raise ValueError('you have not entered email')
        user = self.model(
            email=self.normalize_email(email),
            **extra
        )
        user.set_password(raw_password=password)
        user.save(using=self.db)

    def create(self, email, username, password):
        return self._create(email, username, password)

    def create_superuser(self, email, password):
        return self._create(email, password, is_staff=True, is_superuser=True)
